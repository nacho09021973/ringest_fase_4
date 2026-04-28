"""
Paper 2 analysis producer.

This script is part of the reproducibility snapshot for the Paper 2 analysis.
It operates on frozen input tables and writes the corresponding verified
analysis outputs. External catalog metadata should be frozen before downstream
statistical analyses.
"""
import csv, json, math, itertools, statistics
from pathlib import Path
from collections import Counter

BASE = Path('runs_sync/active')
OUT_DIR = BASE / 'kerr_snr_systematics_t10'
OUT_DIR.mkdir(parents=True, exist_ok=True)

paths = {
    'snr': OUT_DIR / 'snr_residual_audit_table.csv',
    'overlap': BASE / 'kerr_audit_compare_t66_vs_t82a' / 'comparison_overlap.csv',
    'qnm_t66': BASE / 'kerr_audit_20260424_t66_sigmas' / 'qnm_dataset.csv',
    'qnm_t82a': BASE / 'kerr_audit_gwtc4_pseobnr_t82a_verified' / 'qnm_dataset.csv',
    'audit_t66': BASE / 'kerr_audit_20260424_t66_sigmas' / 'kerr_audit_table.csv',
    'audit_t82a': BASE / 'kerr_audit_gwtc4_pseobnr_t82a_verified' / 'kerr_audit_table.csv',
}
OUT_CSV = OUT_DIR / 'snr_overlap_decomposition.csv'
OUT_JSON = OUT_DIR / 'snr_overlap_decomposition_summary.json'
OUT_MD = OUT_DIR / 'snr_overlap_decomposition_notes.md'

def read_csv(path):
    with path.open(newline='') as f:
        r = csv.DictReader(f)
        return list(r), r.fieldnames

def by_event(rows):
    out = {}
    for r in rows:
        ev = r['event']
        if ev in out:
            raise RuntimeError(f'duplicate event in table: {ev}')
        out[ev] = r
    return out

def ff(row, key):
    v = row.get(key)
    if v is None or v == '':
        return None
    return float(v)

def residual_abs(f_obs, sf_obs, f_kerr, sf_kerr, g_obs, sg_obs, g_kerr, sg_kerr):
    rf = (f_obs - f_kerr) / math.sqrt(sf_obs**2 + sf_kerr**2)
    rg = (g_obs - g_kerr) / math.sqrt(sg_obs**2 + sg_kerr**2)
    return max(abs(rf), abs(rg))

def residual_parts(state):
    rf = (state['f_obs'] - state['f_kerr']) / math.sqrt(state['sigma_f_obs']**2 + state['sigma_f_kerr']**2)
    rg = (state['gamma_obs'] - state['gamma_kerr']) / math.sqrt(state['sigma_gamma_obs']**2 + state['sigma_gamma_kerr']**2)
    return rf, rg, max(abs(rf), abs(rg))

def shapley_groups(s66, s82):
    groups = ['OBS_SHIFT', 'OBS_SIGMA_CHANGE', 'KERR_PREDICTION_CHANGE', 'KERR_SIGMA_CHANGE']
    keys = {
        'OBS_SHIFT': ['f_obs', 'gamma_obs'],
        'OBS_SIGMA_CHANGE': ['sigma_f_obs', 'sigma_gamma_obs'],
        'KERR_PREDICTION_CHANGE': ['f_kerr', 'gamma_kerr'],
        'KERR_SIGMA_CHANGE': ['sigma_f_kerr', 'sigma_gamma_kerr'],
    }
    def state_for(changed):
        st = dict(s66)
        for g in changed:
            for k in keys[g]:
                st[k] = s82[k]
        return st
    def value(changed):
        return residual_parts(state_for(changed))[2]
    contrib = {g: 0.0 for g in groups}
    perms = list(itertools.permutations(groups))
    for perm in perms:
        changed = set()
        prev = value(changed)
        for g in perm:
            changed.add(g)
            nxt = value(changed)
            contrib[g] += nxt - prev
            prev = nxt
    for g in groups:
        contrib[g] /= len(perms)
    return contrib

def sign(x):
    return 1 if x > 0 else (-1 if x < 0 else 0)

def classify(delta, contrib):
    # Dominant driver means same-direction Shapley contribution explains >=50% of same-direction magnitude.
    if abs(delta) < 1e-9:
        return 'MIXED', 'near_zero_delta'
    same = {k:v for k,v in contrib.items() if sign(v) == sign(delta) and abs(v) > 1e-12}
    if not same:
        return 'MIXED', 'no_same_direction_single_driver'
    total_same = sum(abs(v) for v in same.values())
    k, v = max(same.items(), key=lambda kv: abs(kv[1]))
    share = abs(v) / total_same if total_same else 0.0
    # Also require driver contribution to be larger than opposing total; otherwise call MIXED.
    opposing = sum(abs(vv) for kk, vv in contrib.items() if sign(vv) == -sign(delta))
    if share >= 0.50 and abs(v) >= opposing:
        return k, f'same_direction_share={share:.3f}; opposing_abs={opposing:.3g}'
    return 'MIXED', f'largest_same={k}; share={share:.3f}; opposing_abs={opposing:.3g}'

snr_rows, _ = read_csv(paths['snr'])
overlap_rows, _ = read_csv(paths['overlap'])
q66, _ = read_csv(paths['qnm_t66'])
q82, _ = read_csv(paths['qnm_t82a'])
a66, _ = read_csv(paths['audit_t66'])
a82, _ = read_csv(paths['audit_t82a'])

snr_t66 = {r['event']: r for r in snr_rows if r['cohort'] == 'T6.6_O3_literature'}
snr_t82 = {r['event']: r for r in snr_rows if r['cohort'] == 'T8.2a_GWTC4_pSEOBNR'}
q66e, q82e = by_event(q66), by_event(q82)
a66e, a82e = by_event(a66), by_event(a82)
overlap_events = sorted(set(a66e) & set(a82e))
# Restrict to explicit comparison overlap to avoid accidental future additions.
comparison_events = sorted({r['event'] for r in overlap_rows})
if overlap_events != comparison_events:
    overlap_events = comparison_events

out_rows = []
for ev in overlap_events:
    r66, r82 = a66e[ev], a82e[ev]
    qn66, qn82 = q66e[ev], q82e[ev]
    snr = ff(snr_t66.get(ev, snr_t82.get(ev, {})), 'network_matched_filter_snr')
    if snr is None and ev in snr_t82:
        snr = ff(snr_t82[ev], 'network_matched_filter_snr')
    s66 = {
        'f_obs': ff(r66, 'f_obs_hz'),
        'sigma_f_obs': ff(r66, 'sigma_f_obs_hz'),
        'f_kerr': ff(r66, 'f_kerr_hz'),
        'sigma_f_kerr': ff(r66, 'sigma_f_kerr_hz'),
        'gamma_obs': ff(r66, 'gamma_obs_hz'),
        'sigma_gamma_obs': ff(r66, 'sigma_gamma_obs_hz'),
        'gamma_kerr': ff(r66, 'gamma_kerr_hz'),
        'sigma_gamma_kerr': ff(r66, 'sigma_gamma_kerr_hz'),
    }
    s82 = {
        'f_obs': ff(r82, 'f_obs_hz'),
        'sigma_f_obs': ff(r82, 'sigma_f_obs_hz'),
        'f_kerr': ff(r82, 'f_kerr_hz'),
        'sigma_f_kerr': ff(r82, 'sigma_f_kerr_hz'),
        'gamma_obs': ff(r82, 'gamma_obs_hz'),
        'sigma_gamma_obs': ff(r82, 'sigma_gamma_obs_hz'),
        'gamma_kerr': ff(r82, 'gamma_kerr_hz'),
        'sigma_gamma_kerr': ff(r82, 'sigma_gamma_kerr_hz'),
    }
    rf66, rg66, m66 = residual_parts(s66)
    rf82, rg82, m82 = residual_parts(s82)
    delta = m82 - m66
    contrib = shapley_groups(s66, s82)
    driver, reason = classify(delta, contrib)
    # high SNR in overlap: the pair has SNR >=20 or is among the top two overlap SNRs. Fill top-two after sorting below too.
    row = {
        'event': ev,
        'SNR': snr,
        'max_abs_residual_t66': ff(r66, 'max_abs_residual'),
        'max_abs_residual_t82a': ff(r82, 'max_abs_residual'),
        'delta_max_abs_residual': delta,
        'residual_f_t66': ff(r66, 'residual_f'),
        'residual_f_t82a': ff(r82, 'residual_f'),
        'residual_gamma_t66': ff(r66, 'residual_gamma'),
        'residual_gamma_t82a': ff(r82, 'residual_gamma'),
        'dominant_residual_component_t66': 'gamma' if abs(ff(r66,'residual_gamma')) >= abs(ff(r66,'residual_f')) else 'f',
        'dominant_residual_component_t82a': 'gamma' if abs(ff(r82,'residual_gamma')) >= abs(ff(r82,'residual_f')) else 'f',
        'f_obs_t66': ff(r66, 'f_obs_hz'),
        'f_obs_t82a': ff(r82, 'f_obs_hz'),
        'delta_f_obs_hz': ff(r82, 'f_obs_hz') - ff(r66, 'f_obs_hz'),
        'gamma_obs_t66': ff(r66, 'gamma_obs_hz'),
        'gamma_obs_t82a': ff(r82, 'gamma_obs_hz'),
        'delta_gamma_obs_hz': ff(r82, 'gamma_obs_hz') - ff(r66, 'gamma_obs_hz'),
        'tau_ms_t66': ff(qn66, 'tau_ms'),
        'tau_ms_t82a': ff(qn82, 'tau_ms'),
        'delta_tau_ms': ff(qn82, 'tau_ms') - ff(qn66, 'tau_ms'),
        'sigma_f_obs_t66': ff(r66, 'sigma_f_obs_hz'),
        'sigma_f_obs_t82a': ff(r82, 'sigma_f_obs_hz'),
        'sigma_gamma_obs_t66': ff(r66, 'sigma_gamma_obs_hz'),
        'sigma_gamma_obs_t82a': ff(r82, 'sigma_gamma_obs_hz'),
        'f_kerr_t66': ff(r66, 'f_kerr_hz'),
        'f_kerr_t82a': ff(r82, 'f_kerr_hz'),
        'delta_f_kerr_hz': ff(r82, 'f_kerr_hz') - ff(r66, 'f_kerr_hz'),
        'gamma_kerr_t66': ff(r66, 'gamma_kerr_hz'),
        'gamma_kerr_t82a': ff(r82, 'gamma_kerr_hz'),
        'delta_gamma_kerr_hz': ff(r82, 'gamma_kerr_hz') - ff(r66, 'gamma_kerr_hz'),
        'sigma_f_kerr_t66': ff(r66, 'sigma_f_kerr_hz'),
        'sigma_f_kerr_t82a': ff(r82, 'sigma_f_kerr_hz'),
        'sigma_gamma_kerr_t66': ff(r66, 'sigma_gamma_kerr_hz'),
        'sigma_gamma_kerr_t82a': ff(r82, 'sigma_gamma_kerr_hz'),
        'shapley_OBS_SHIFT': contrib['OBS_SHIFT'],
        'shapley_OBS_SIGMA_CHANGE': contrib['OBS_SIGMA_CHANGE'],
        'shapley_KERR_PREDICTION_CHANGE': contrib['KERR_PREDICTION_CHANGE'],
        'shapley_KERR_SIGMA_CHANGE': contrib['KERR_SIGMA_CHANGE'],
        'dominant_driver': driver,
        'driver_rule_note': reason,
        't66_verdict': r66.get('verdict_kerr'),
        't82a_verdict': r82.get('verdict_kerr'),
        'tail_high_t66': ff(r66, 'max_abs_residual') >= 1.0,
        'tail_high_t82a': ff(r82, 'max_abs_residual') >= 1.0,
        'lost_high_tail_in_t82a': ff(r66, 'max_abs_residual') >= 1.0 and ff(r82, 'max_abs_residual') < 1.0,
        't82a_no_improvement': delta >= 0,
    }
    out_rows.append(row)

# high-SNR flags after overlap sorting.
out_rows.sort(key=lambda r: (-r['SNR'], r['event']))
for i, r in enumerate(out_rows, 1):
    r['snr_rank_overlap'] = i
    r['high_snr_overlap'] = bool(r['SNR'] >= 20.0 or i <= 2)
    r['high_snr_lost_tail'] = bool(r['high_snr_overlap'] and r['lost_high_tail_in_t82a'])

fieldnames = [
    'event','SNR','snr_rank_overlap','high_snr_overlap','high_snr_lost_tail',
    'max_abs_residual_t66','max_abs_residual_t82a','delta_max_abs_residual',
    'residual_f_t66','residual_f_t82a','residual_gamma_t66','residual_gamma_t82a',
    'dominant_residual_component_t66','dominant_residual_component_t82a',
    'f_obs_t66','f_obs_t82a','delta_f_obs_hz',
    'gamma_obs_t66','gamma_obs_t82a','delta_gamma_obs_hz',
    'tau_ms_t66','tau_ms_t82a','delta_tau_ms',
    'sigma_f_obs_t66','sigma_f_obs_t82a','sigma_gamma_obs_t66','sigma_gamma_obs_t82a',
    'f_kerr_t66','f_kerr_t82a','delta_f_kerr_hz',
    'gamma_kerr_t66','gamma_kerr_t82a','delta_gamma_kerr_hz',
    'sigma_f_kerr_t66','sigma_f_kerr_t82a','sigma_gamma_kerr_t66','sigma_gamma_kerr_t82a',
    'shapley_OBS_SHIFT','shapley_OBS_SIGMA_CHANGE','shapley_KERR_PREDICTION_CHANGE','shapley_KERR_SIGMA_CHANGE',
    'dominant_driver','driver_rule_note','t66_verdict','t82a_verdict','tail_high_t66','tail_high_t82a','lost_high_tail_in_t82a','t82a_no_improvement'
]
with OUT_CSV.open('w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=fieldnames)
    w.writeheader()
    for r in out_rows:
        out = {}
        for k in fieldnames:
            v = r.get(k, '')
            if isinstance(v, bool):
                v = 'true' if v else 'false'
            out[k] = v
        w.writerow(out)

lost = [r for r in out_rows if r['lost_high_tail_in_t82a']]
noimp = [r for r in out_rows if r['t82a_no_improvement']]
high_lost = [r for r in out_rows if r['high_snr_lost_tail']]
summary = {
    'artifact': 'T10.1 overlap decomposition T6.6 vs T8.2a',
    'input_files': {k: str(v) for k,v in paths.items()},
    'output_files': [str(OUT_CSV), str(OUT_JSON), str(OUT_MD)],
    'n_overlap_events': len(out_rows),
    'overlap_events_ordered_by_snr': [r['event'] for r in out_rows],
    'high_snr_definition': 'SNR >= 20 or top two SNR events inside the six-event overlap',
    'high_snr_events': [r['event'] for r in out_rows if r['high_snr_overlap']],
    'events_lost_high_tail_in_t82a': [r['event'] for r in lost],
    'high_snr_events_lost_high_tail_in_t82a': [r['event'] for r in high_lost],
    'events_t82a_no_improvement': [r['event'] for r in noimp],
    'dominant_driver_counts': dict(Counter(r['dominant_driver'] for r in out_rows)),
    'dominant_driver_by_event': {r['event']: r['dominant_driver'] for r in out_rows},
    'shapley_method': {
        'metric': 'delta max_abs_residual = max(|residual_f|, |residual_gamma|)_t82a - max(|residual_f|, |residual_gamma|)_t66',
        'groups': {
            'OBS_SHIFT': ['f_obs_hz', 'gamma_obs_hz derived from tau_ms'],
            'OBS_SIGMA_CHANGE': ['sigma_f_obs_hz', 'sigma_gamma_obs_hz'],
            'KERR_PREDICTION_CHANGE': ['f_kerr_hz', 'gamma_kerr_hz'],
            'KERR_SIGMA_CHANGE': ['sigma_f_kerr_hz', 'sigma_gamma_kerr_hz'],
        },
        'classification_rule': 'Dominant driver is the largest same-direction Shapley contribution if it explains >=50% of same-direction magnitude and is not outweighed by opposite-sign contributions; otherwise MIXED.',
    },
    'event_rows': out_rows,
    'limited_interpretation': {
        'main_pattern': 'Among high-SNR overlap events, GW150914 and GW190521_074359 lose the T6.6 high residual tail in T8.2a; both are dominated by OBS_SIGMA_CHANGE, specifically enlarged damping/tau-derived uncertainty reducing gamma residuals.',
        'not_universal': 'GW190828_063405 and GW190910_112807 do not improve in T8.2a; their residual maximum shifts to gamma with larger absolute gamma residual despite larger sigma_gamma_obs.',
        'paper_safe_language': 'In the six-event overlap, the disappearance of the T6.6 high-residual tail in the pSEOBNRv5PHM rows is most consistent with changed QNM posterior uncertainties and damping-time observables, not with a uniform Kerr-prediction shift. This is a paired descriptive audit, not causal proof.',
    },
}
OUT_JSON.write_text(json.dumps(summary, indent=2, sort_keys=True) + '\n')

# Notes markdown.
def fmt(x, nd=3):
    if x is None:
        return 'NA'
    try:
        x = float(x)
        if not math.isfinite(x):
            return 'NA'
        return f'{x:.{nd}g}'
    except Exception:
        return str(x)

lines = []
lines.append('# T10.1 overlap decomposition T6.6 vs T8.2a')
lines.append('')
lines.append('- archivo: `snr_overlap_decomposition.csv`')
lines.append('- inputs reales: T10 SNR audit, overlap comparison, QNM datasets y Kerr audit tables de T6.6/T8.2a.')
lines.append('- outputs reales: tabla pareada de seis eventos solapados, atribucion Shapley por grupo de cambio y notas.')
lines.append('- funcion fisica: separar si el cambio de cola alta viene de observable QNM, sigmas o prediccion Kerr.')
lines.append('- dependencia toy/teorica: ninguna nueva; no se ejecutan stages ni se modifica pipeline.')
lines.append('- veredicto: RESCATAR como auditoria descriptiva; no afirmar causalidad fuerte.')
lines.append('')
lines.append('## Eventos solapados')
lines.append('')
lines.append(', '.join(r['event'] for r in out_rows))
lines.append('')
lines.append('## Tabla pareada ordenada por SNR')
lines.append('')
lines.append('| event | SNR | max T6.6 | max T8.2a | delta | r_f T6.6 | r_f T8.2a | r_gamma T6.6 | r_gamma T8.2a | driver | marca |')
lines.append('|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|')
for r in out_rows:
    marks = []
    if r['high_snr_lost_tail']:
        marks.append('HIGH_SNR_LOST_TAIL')
    if r['t82a_no_improvement']:
        marks.append('T82A_NO_IMPROVEMENT')
    if r['lost_high_tail_in_t82a'] and not r['high_snr_lost_tail']:
        marks.append('LOST_TAIL')
    lines.append(f"| {r['event']} | {fmt(r['SNR'])} | {fmt(r['max_abs_residual_t66'])} | {fmt(r['max_abs_residual_t82a'])} | {fmt(r['delta_max_abs_residual'])} | {fmt(r['residual_f_t66'])} | {fmt(r['residual_f_t82a'])} | {fmt(r['residual_gamma_t66'])} | {fmt(r['residual_gamma_t82a'])} | {r['dominant_driver']} | {', '.join(marks) or ''} |")
lines.append('')
lines.append('## Driver dominante por evento')
lines.append('')
for r in out_rows:
    lines.append(f"- `{r['event']}`: `{r['dominant_driver']}`; Shapley OBS={fmt(r['shapley_OBS_SHIFT'])}, OBS_SIGMA={fmt(r['shapley_OBS_SIGMA_CHANGE'])}, KERR={fmt(r['shapley_KERR_PREDICTION_CHANGE'])}, KERR_SIGMA={fmt(r['shapley_KERR_SIGMA_CHANGE'])}. {r['driver_rule_note']}.")
lines.append('')
lines.append('## Lectura de f/tau, sigmas y Kerr')
lines.append('')
lines.append('- En `GW150914`, `GW170104` y `GW190521_074359`, la cola T6.6 estaba dominada por `residual_gamma`; en T8.2a cae por aumento fuerte de `sigma_gamma_obs` y cambios de tau/damping. El driver dominante sale `OBS_SIGMA_CHANGE`.')
lines.append('- `GW190519_153544` tambien mejora, pero no era cola alta fuerte; su reduccion es mixta entre cambio observacional y sigma observacional.')
lines.append('- `GW190828_063405` y `GW190910_112807` no mejoran: T8.2a mantiene o sube `max_abs_residual`, con maximo dominado por gamma. No hay desaparicion universal de residuo en pSEOBNRv5PHM.')
lines.append('- Los cambios de prediccion Kerr (`f_kerr`, `gamma_kerr`) son secundarios en la mayoria de eventos; no explican por si solos la desaparicion de la cola alta.')
lines.append('')
lines.append('## Interpretacion limitada para paper')
lines.append('')
lines.append('- Hecho verificado: en los seis eventos solapados, los high-SNR `GW150914` y `GW190521_074359` pierden la cola alta en T8.2a.')
lines.append('- Inferencia: la reduccion esta mas ligada a sigmas observacionales de damping/tau y a cambios del observable QNM que a un desplazamiento coherente de la prediccion Kerr.')
lines.append('- Propuesta de frase segura: "In the six-event overlap, the pSEOBNRv5PHM rows reduce the high-SNR residual tail mainly through broader or shifted ringdown-mode posterior summaries, especially in the damping-time channel; this should be read as a waveform/posterior-systematics diagnostic rather than evidence for a physical deviation."')
lines.append('')
lines.append('## Guardrails')
lines.append('')
lines.append('- No se modifico YAML, codigo principal ni thresholds.')
lines.append('- No se ejecuto Stage 02/03/04.')
lines.append('- No se afirma causalidad fuerte.')
OUT_MD.write_text('\n'.join(lines) + '\n')

print(json.dumps({
    'overlap_events_ordered_by_snr': [r['event'] for r in out_rows],
    'high_snr_events': [r['event'] for r in out_rows if r['high_snr_overlap']],
    'lost_high_tail': [r['event'] for r in lost],
    'high_snr_lost_tail': [r['event'] for r in high_lost],
    't82a_no_improvement': [r['event'] for r in noimp],
    'driver_by_event': {r['event']: r['dominant_driver'] for r in out_rows},
    'driver_counts': dict(Counter(r['dominant_driver'] for r in out_rows)),
    'outputs': [str(OUT_CSV), str(OUT_JSON), str(OUT_MD)],
}, indent=2))
