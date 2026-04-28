"""
Paper 2 analysis producer.

This script is part of the reproducibility snapshot for the Paper 2 analysis.
It operates on frozen input tables and writes the corresponding verified
analysis outputs. External catalog metadata should be frozen before downstream
statistical analyses.
"""
import csv, json, time, urllib.request
from datetime import datetime, timezone
from pathlib import Path

out_dir = Path('runs_sync/active/kerr_population_tail_t9')
input_path = out_dir / 't9_base_residual_table.csv'
output_csv = out_dir / 'population_metadata_table.csv'
coverage_json = out_dir / 'population_metadata_coverage.json'
notes_md = out_dir / 'population_metadata_notes.md'
api_base = 'https://gwosc.org/api/v2'

population_fields = ['mass_1_source', 'mass_2_source', 'chi_eff', 'chi_p', 'redshift']
search_fields = ['network_matched_filter_snr', 'network_snr', 'p_astro', 'far']
requested_fields = population_fields + search_fields + ['M_total_source', 'q']

def catalog_rank(catalog):
    c = catalog or ''
    if 'GWTC-3-confident' in c:
        return 900
    if 'GWTC-2.1-confident' in c:
        return 800
    if c == 'GWTC-2' or c.startswith('GWTC-2'):
        return 700
    if 'GWTC-1-confident' in c:
        return 600
    if 'O3_Discovery_Papers' in c:
        return 500
    if 'O1_O2-Preliminary' in c:
        return 400
    if 'IAS' in c:
        return 300
    return 0

search_pipeline_rank = {
    'gstlal': 100,
    'gstlal_allsky': 99,
    'pycbc_bbh': 90,
    'pycbc': 89,
    'pycbc_broad': 88,
    'pycbc_allsky': 87,
    'pycbc_highmass': 86,
    'mbta': 80,
    'cwb': 70,
    'cwb_allsky': 69,
}

cache = {}
def get_json(url, retries=4):
    if url in cache:
        return cache[url]
    last = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'RINGEST-T9.1-metadata-audit/1.1'})
            with urllib.request.urlopen(req, timeout=45) as resp:
                data = json.load(resp)
            cache[url] = data
            return data
        except Exception as exc:
            last = exc
            time.sleep(1.0 + attempt)
    raise last

def params_map(result):
    return {p.get('name'): p.get('best') for p in (result.get('parameters') or []) if p.get('name')}

def result_name(result):
    return result.get('name') or ''

def version_id(version):
    return (version.get('detail_url') or '').rstrip('/').split('/')[-1]

def version_num(version):
    try:
        return int(version_id(version).rsplit('-v', 1)[1])
    except Exception:
        return version.get('version') or 0

with input_path.open(newline='') as f:
    reader = csv.DictReader(f)
    rows = list(reader)
    input_fields = reader.fieldnames or []

events = sorted({row['event'] for row in rows})
metadata_by_event = {}
errors = {}

for ev in events:
    try:
        event_json = get_json(f'{api_base}/events/{ev}')
        versions = event_json.get('versions') or []
        version_payloads = []
        for v in versions:
            vid = version_id(v)
            if not vid:
                continue
            try:
                payload = get_json(f'{api_base}/event-versions/{vid}/parameters')
            except Exception as exc:
                version_payloads.append({'version': v, 'version_id': vid, 'error': str(exc), 'results': []})
                continue
            version_payloads.append({'version': v, 'version_id': vid, 'error': None, 'results': payload.get('results') or []})

        pe_candidates = []
        search_candidates = []
        for vp in version_payloads:
            v = vp['version']
            for res in vp['results']:
                pmap = params_map(res)
                common_pop = sum(1 for k in ['mass_1_source', 'mass_2_source', 'chi_eff', 'redshift'] if pmap.get(k) is not None)
                common_search = sum(1 for k in search_fields if pmap.get(k) is not None)
                base = {
                    'version': v,
                    'version_id': vp['version_id'],
                    'catalog': v.get('catalog'),
                    'result': res,
                    'params': pmap,
                    'rank': catalog_rank(v.get('catalog')),
                    'version_num': version_num(v),
                }
                if (res.get('pipeline_type') == 'pe' or common_pop) and common_pop:
                    cand = dict(base)
                    cand['pop_count'] = common_pop + (1 if pmap.get('chi_p') is not None else 0)
                    cand['preferred'] = 1 if res.get('is_preferred') else 0
                    pe_candidates.append(cand)
                # p_astro/FAR are detection-pipeline quantities; do not let PE-only SNR rows mask search rows.
                if res.get('pipeline_type') == 'search' and common_search:
                    cand = dict(base)
                    cand['search_count'] = common_search
                    cand['pipeline_rank'] = search_pipeline_rank.get(res.get('pipeline') or '', 0)
                    cand['preferred'] = 1 if res.get('is_preferred') else 0
                    cand['detection_score'] = (
                        (20 if pmap.get('p_astro') is not None else 0) +
                        (20 if pmap.get('far') is not None else 0) +
                        (10 if pmap.get('network_matched_filter_snr') is not None else 0) +
                        (10 if pmap.get('network_snr') is not None else 0)
                    )
                    search_candidates.append(cand)

        pe_candidates.sort(key=lambda c: (c['rank'], c['preferred'], c['pop_count'], c['version_num']), reverse=True)
        selected_pe = pe_candidates[0] if pe_candidates else None

        selected_search = None
        if search_candidates:
            same_catalog = [c for c in search_candidates if selected_pe and c['catalog'] == selected_pe['catalog']]
            pool = same_catalog or search_candidates
            pool.sort(key=lambda c: (c['rank'], c['detection_score'], c['pipeline_rank'], c['version_num']), reverse=True)
            selected_search = pool[0]

        vals = {k: None for k in requested_fields}
        if selected_pe:
            p = selected_pe['params']
            for k in population_fields:
                vals[k] = p.get(k)
            for k in ['network_matched_filter_snr', 'network_snr']:
                if p.get(k) is not None:
                    vals[k] = p.get(k)
        if selected_search:
            p = selected_search['params']
            for k in search_fields:
                if vals.get(k) is None and p.get(k) is not None:
                    vals[k] = p.get(k)

        m1, m2 = vals.get('mass_1_source'), vals.get('mass_2_source')
        if m1 is not None and m2 is not None:
            vals['M_total_source'] = float(m1) + float(m2)
            hi, lo = max(float(m1), float(m2)), min(float(m1), float(m2))
            vals['q'] = lo / hi if hi else None

        core = ['mass_1_source', 'mass_2_source', 'chi_eff', 'redshift', 'M_total_source', 'q']
        snr_ok = vals.get('network_matched_filter_snr') is not None or vals.get('network_snr') is not None
        detection_ok = vals.get('p_astro') is not None or vals.get('far') is not None
        if not selected_pe and not selected_search:
            status = 'MISSING'
        elif all(vals.get(k) is not None for k in core) and snr_ok and detection_ok:
            status = 'SOURCE_OK'
        else:
            status = 'PARTIAL'

        metadata_by_event[ev] = {
            **vals,
            'metadata_status': status,
            'chi_p_available': bool(vals.get('chi_p') is not None),
            'pe_catalog_source': selected_pe['catalog'] if selected_pe else '',
            'pe_version_source': selected_pe['version_id'] if selected_pe else '',
            'pe_result_source': result_name(selected_pe['result']) if selected_pe else '',
            'pe_pipeline_source': selected_pe['result'].get('pipeline') if selected_pe else '',
            'search_catalog_source': selected_search['catalog'] if selected_search else '',
            'search_version_source': selected_search['version_id'] if selected_search else '',
            'search_result_source': result_name(selected_search['result']) if selected_search else '',
            'search_pipeline_source': selected_search['result'].get('pipeline') if selected_search else '',
            'gwosc_versions': [version_id(v) for v in versions],
            'gwosc_catalogs': [v.get('catalog') for v in versions],
            'version_errors': [f"{vp['version_id']}: {vp['error']}" for vp in version_payloads if vp.get('error')],
        }
    except Exception as exc:
        errors[ev] = str(exc)
        metadata_by_event[ev] = {
            **{k: None for k in requested_fields},
            'metadata_status': 'MISSING',
            'chi_p_available': False,
            'pe_catalog_source': '', 'pe_version_source': '', 'pe_result_source': '', 'pe_pipeline_source': '',
            'search_catalog_source': '', 'search_version_source': '', 'search_result_source': '', 'search_pipeline_source': '',
            'gwosc_versions': [], 'gwosc_catalogs': [], 'version_errors': [str(exc)],
        }

append_fields = [
    'mass_1_source', 'mass_2_source', 'M_total_source', 'q',
    'chi_eff', 'chi_p', 'chi_p_available',
    'network_matched_filter_snr', 'network_snr',
    'redshift', 'p_astro', 'FAR', 'metadata_status',
    'pe_catalog_source', 'pe_version_source', 'pe_result_source', 'pe_pipeline_source',
    'search_catalog_source', 'search_version_source', 'search_result_source', 'search_pipeline_source',
]
fieldnames = input_fields + [f for f in append_fields if f not in input_fields]

out_rows = []
for row in rows:
    ev = row['event']
    md = metadata_by_event[ev]
    out = dict(row)
    for f in append_fields:
        key = 'far' if f == 'FAR' else f
        val = md.get(key)
        if isinstance(val, bool):
            out[f] = 'true' if val else 'false'
        elif val is None:
            out[f] = ''
        else:
            out[f] = val
    out_rows.append(out)

with output_csv.open('w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(out_rows)

field_coverage = {}
coverage_fields = ['mass_1_source', 'mass_2_source', 'M_total_source', 'q', 'chi_eff', 'chi_p', 'network_matched_filter_snr', 'network_snr', 'redshift', 'p_astro', 'far']
for field in coverage_fields:
    n_events = sum(1 for ev in events if metadata_by_event[ev].get(field) is not None)
    n_rows = sum(1 for r in out_rows if r.get('FAR' if field == 'far' else field) not in ('', None))
    field_coverage['FAR' if field == 'far' else field] = {
        'events': n_events,
        'event_fraction': n_events / len(events) if events else 0,
        'rows': n_rows,
        'row_fraction': n_rows / len(out_rows) if out_rows else 0,
    }
network_any_events = sum(1 for ev in events if metadata_by_event[ev].get('network_matched_filter_snr') is not None or metadata_by_event[ev].get('network_snr') is not None)
network_any_rows = sum(1 for r in out_rows if r.get('network_matched_filter_snr') or r.get('network_snr'))
detection_any_events = sum(1 for ev in events if metadata_by_event[ev].get('p_astro') is not None or metadata_by_event[ev].get('far') is not None)
detection_any_rows = sum(1 for r in out_rows if r.get('p_astro') or r.get('FAR'))
field_coverage['network_snr_any'] = {
    'events': network_any_events,
    'event_fraction': network_any_events / len(events) if events else 0,
    'rows': network_any_rows,
    'row_fraction': network_any_rows / len(out_rows) if out_rows else 0,
}
field_coverage['p_astro_or_FAR'] = {
    'events': detection_any_events,
    'event_fraction': detection_any_events / len(events) if events else 0,
    'rows': detection_any_rows,
    'row_fraction': detection_any_rows / len(out_rows) if out_rows else 0,
}

status_counts = {}
for ev in events:
    st = metadata_by_event[ev]['metadata_status']
    status_counts[st] = status_counts.get(st, 0) + 1

incomplete_events = [ev for ev in events if metadata_by_event[ev]['metadata_status'] != 'SOURCE_OK']
chi_p_events = [ev for ev in events if metadata_by_event[ev].get('chi_p') is not None]
chi_p_fraction = len(chi_p_events) / len(events) if events else 0

coverage = {
    'artifact': 'T9.1 GWOSC population metadata enrichment',
    'generated_utc': datetime.now(timezone.utc).isoformat(),
    'input_file': str(input_path),
    'outputs': {'table_csv': str(output_csv), 'coverage_json': str(coverage_json), 'notes_md': str(notes_md)},
    'gwosc_api_base': api_base,
    'selection_policy': {
        'population_metadata': 'Preferred PE result from highest-ranked official GWTC/confident catalog available; IAS only fallback when no official catalog is available.',
        'snr_metadata': 'Use network_matched_filter_snr/network_snr from selected PE if present; otherwise allow selected search result.',
        'detection_metadata': 'Use p_astro/FAR only from pipeline_type=search results. Prefer the same selected catalog when available; otherwise use the highest-ranked search catalog with deterministic pipeline priority gstlal > pycbc_bbh > pycbc > pycbc_broad > pycbc_allsky > pycbc_highmass > mbta > cwb.',
        'metadata_status': 'SOURCE_OK requires mass_1_source, mass_2_source, chi_eff, redshift, derived M_total_source/q, any network SNR, and p_astro or FAR. chi_p is tracked separately and does not make all rows PARTIAL by itself.',
    },
    'n_input_rows': len(rows),
    'n_unique_events': len(events),
    'events_consulted': events,
    'field_coverage': field_coverage,
    'metadata_status_counts_by_event': status_counts,
    'events_with_incomplete_metadata': incomplete_events,
    'chi_p_available_events': chi_p_events,
    'chi_p_event_fraction': chi_p_fraction,
    'chi_p_covers_at_least_80_percent': chi_p_fraction >= 0.8,
    'recommendation_for_T9_2_chi_p': 'USE' if chi_p_fraction >= 0.8 else 'PARK_CHI_P',
    'selected_sources_by_event': {
        ev: {
            'metadata_status': metadata_by_event[ev]['metadata_status'],
            'pe_catalog_source': metadata_by_event[ev]['pe_catalog_source'],
            'pe_version_source': metadata_by_event[ev]['pe_version_source'],
            'pe_result_source': metadata_by_event[ev]['pe_result_source'],
            'pe_pipeline_source': metadata_by_event[ev]['pe_pipeline_source'],
            'search_catalog_source': metadata_by_event[ev]['search_catalog_source'],
            'search_version_source': metadata_by_event[ev]['search_version_source'],
            'search_result_source': metadata_by_event[ev]['search_result_source'],
            'search_pipeline_source': metadata_by_event[ev]['search_pipeline_source'],
            'gwosc_versions': metadata_by_event[ev]['gwosc_versions'],
            'gwosc_catalogs': metadata_by_event[ev]['gwosc_catalogs'],
            'version_errors': metadata_by_event[ev]['version_errors'],
        } for ev in events
    },
    'query_errors': errors,
}
with coverage_json.open('w') as f:
    json.dump(coverage, f, indent=2, sort_keys=True)
    f.write('\n')

lines = []
lines.append('# T9.1 GWOSC population metadata enrichment')
lines.append('')
lines.append('- archivo: `population_metadata_table.csv`')
lines.append('- inputs reales: `t9_base_residual_table.csv` y GWOSC API v2 (`/events/{event}`, `/event-versions/{version}/parameters`).')
lines.append('- outputs reales: metadata poblacional por fila event x cohort, cobertura JSON y estas notas.')
lines.append('- funcion fisica: anotar masas fuente, razon de masas, spin efectivo, redshift, SNR y significancia de busqueda para auditoria poblacional posterior; no ejecuta correlaciones ni claims.')
lines.append('- dependencia toy/teorica: ninguna nueva; esto solo enriquece filas Kerr/Ruta C ya existentes con metadata catalogal.')
lines.append('- veredicto: RESCATAR como capa exploratoria T9.1; no confirma familia fisica.')
lines.append('')
lines.append('## Regla de seleccion')
lines.append('')
lines.append('- Poblacion: resultado PE preferido del catalogo oficial GWTC/confident de mayor prioridad disponible. IAS-O3a queda solo como fallback si no hay GWTC oficial.')
lines.append('- SNR: `network_matched_filter_snr`/`network_snr` desde el PE seleccionado si esta; si no, desde el resultado search seleccionado.')
lines.append('- Busqueda: `p_astro`/FAR solo desde resultados `pipeline_type=search`. Se usa el mismo catalogo que el PE si existe; si no, el mejor search catalogal disponible con prioridad gstlal, pycbc_bbh, pycbc, pycbc_broad, pycbc_allsky, pycbc_highmass, mbta, cwb.')
lines.append('- `metadata_status=SOURCE_OK` exige masas fuente, `chi_eff`, `redshift`, `M_total_source`, `q`, algun SNR de red y `p_astro` o FAR. `chi_p` se evalua aparte mediante `chi_p_available`.')
lines.append('')
lines.append('## Eventos consultados')
lines.append('')
lines.append(', '.join(events))
lines.append('')
lines.append('## Cobertura por campo')
lines.append('')
for field in ['mass_1_source', 'mass_2_source', 'M_total_source', 'q', 'chi_eff', 'chi_p', 'network_matched_filter_snr', 'network_snr', 'network_snr_any', 'redshift', 'p_astro', 'FAR', 'p_astro_or_FAR']:
    c = field_coverage[field]
    lines.append(f'- `{field}`: {c["events"]}/{len(events)} eventos ({100*c["event_fraction"]:.1f}%), {c["rows"]}/{len(out_rows)} filas ({100*c["row_fraction"]:.1f}%)')
lines.append('')
lines.append('## Metadata incompleta')
lines.append('')
if incomplete_events:
    for ev in incomplete_events:
        md = metadata_by_event[ev]
        missing = []
        for field in ['mass_1_source', 'mass_2_source', 'chi_eff', 'redshift', 'M_total_source', 'q']:
            if md.get(field) is None:
                missing.append(field)
        if md.get('network_matched_filter_snr') is None and md.get('network_snr') is None:
            missing.append('network_snr_any')
        if md.get('p_astro') is None and md.get('far') is None:
            missing.append('p_astro_or_FAR')
        lines.append(f'- `{ev}`: {md["metadata_status"]}; faltan {", ".join(missing) if missing else "campos no-core"}')
else:
    lines.append('- Ningun evento queda incompleto segun la definicion T9.1 usada aqui.')
lines.append('')
lines.append('## chi_p')
lines.append('')
lines.append(f'- `chi_p_available=true`: {len(chi_p_events)}/{len(events)} eventos ({100*chi_p_fraction:.1f}%).')
lines.append(f'- Cubre >=80%: {"true" if chi_p_fraction >= 0.8 else "false"}.')
lines.append(f'- Recomendacion T9.2: {"usar chi_p" if chi_p_fraction >= 0.8 else "aparcar chi_p"}; la API GWOSC v2 no expone `chi_p` para esta muestra con el nombre solicitado.')
lines.append('')
lines.append('## Limitaciones')
lines.append('')
lines.append('- No se modifico YAML canonico, codigo principal, thresholds ni stages 02/03/04.')
lines.append('- No se reextrajeron QNM.')
lines.append('- FAR y `p_astro` son dependientes del pipeline de busqueda seleccionado; las fuentes quedan en columnas `search_*_source`.')
lines.append('- En O1/O2, si el PE preferido viene de GWTC-2.1 pero no hay resultado search en ese catalogo, `p_astro`/FAR se rellenan desde el search GWTC-1 disponible.')
lines.append('- Este output es exploratorio: no hay correlaciones, regresiones ni claims fisicos.')
notes_md.write_text('\n'.join(lines) + '\n')

print(json.dumps({
    'events': events,
    'n_rows': len(rows),
    'n_events': len(events),
    'status_counts': status_counts,
    'chi_p_fraction': chi_p_fraction,
    'incomplete_events': incomplete_events,
    'outputs': [str(output_csv), str(coverage_json), str(notes_md)],
}, indent=2))
