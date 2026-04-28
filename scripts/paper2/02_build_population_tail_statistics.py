"""
Paper 2 analysis producer.

This script is part of the reproducibility snapshot for the Paper 2 analysis.
It operates on frozen input tables and writes the corresponding verified
analysis outputs. External catalog metadata should be frozen before downstream
statistical analyses.
"""
import csv, json, math, itertools, statistics, random
from pathlib import Path
from collections import Counter, defaultdict

import numpy as np

BASE = Path('runs_sync/active/kerr_population_tail_t9')
INPUT = BASE / 'population_metadata_table.csv'
COVERAGE = BASE / 'population_metadata_coverage.json'
NOTES_IN = BASE / 'population_metadata_notes.md'
OUT_CSV = BASE / 'population_tail_stats_table.csv'
OUT_JSON = BASE / 'population_tail_summary.json'
OUT_MD = BASE / 'population_tail_notes.md'

PERMUTATIONS = 20000
RNG_SEED = 9021
TOP_TERTILE_THRESHOLD = 2/3
SHRINKAGE_ALPHA = 0.10
COND_MAX = 1e6
EPS = 1e-12

# ---------- basic utilities ----------
def to_float(x):
    if x is None or x == '':
        return None
    return float(x)

def logit(p):
    p = min(max(float(p), EPS), 1.0 - EPS)
    return math.log(p / (1.0 - p))

def ranks_average(values):
    # 1-indexed average ranks, ties averaged.
    vals = list(values)
    order = sorted(range(len(vals)), key=lambda i: vals[i])
    ranks = [None] * len(vals)
    i = 0
    while i < len(order):
        j = i + 1
        while j < len(order) and vals[order[j]] == vals[order[i]]:
            j += 1
        avg = (i + 1 + j) / 2.0
        for k in range(i, j):
            ranks[order[k]] = avg
        i = j
    return ranks

def pearson(x, y):
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    if len(x) < 3:
        return float('nan')
    sx = x.std(ddof=0)
    sy = y.std(ddof=0)
    if sx == 0 or sy == 0:
        return float('nan')
    return float(np.mean((x - x.mean()) * (y - y.mean())) / (sx * sy))

def spearman(x, y):
    if len(x) < 3:
        return float('nan')
    rx = ranks_average(x)
    ry = ranks_average(y)
    return pearson(rx, ry)

def perm_p_positive(x, y, obs, n_perm=PERMUTATIONS, seed=RNG_SEED):
    if len(x) < 4 or not math.isfinite(obs):
        return None, 0
    rng = random.Random(seed + len(x) * 1009 + int(sum(ranks_average(x)) * 17))
    y = list(y)
    count = 0
    for _ in range(n_perm):
        yy = y[:]
        rng.shuffle(yy)
        rr = spearman(x, yy)
        if math.isfinite(rr) and rr >= obs:
            count += 1
    return (count + 1) / (n_perm + 1), n_perm

def theil_sen_slope(x, y):
    slopes = []
    for i in range(len(x)):
        for j in range(i + 1, len(x)):
            dx = x[j] - x[i]
            if dx != 0:
                slopes.append((y[j] - y[i]) / dx)
    if not slopes:
        return float('nan')
    return float(statistics.median(slopes))

def binom_tail_geq(k, n, p):
    if n <= 0:
        return None
    total = 0.0
    for i in range(k, n + 1):
        total += math.comb(n, i) * (p ** i) * ((1 - p) ** (n - i))
    return total

def group_label(rows):
    vals = sorted({r['cohort'] for r in rows})
    return vals[0] if len(vals) == 1 else 'COMBINED'

# ---------- read inputs ----------
with INPUT.open(newline='') as f:
    reader = csv.DictReader(f)
    rows = list(reader)
    input_fields = reader.fieldnames or []
coverage = json.loads(COVERAGE.read_text())

# Preserve row ids.
for i, row in enumerate(rows):
    row['_row_id'] = i

# ---------- event-level primary feature matrix ----------
event_meta = {}
for row in rows:
    ev = row['event']
    vals = {
        'M_total_source': to_float(row['M_total_source']),
        'q': to_float(row['q']),
        'chi_eff': to_float(row['chi_eff']),
        'redshift': to_float(row['redshift']),
    }
    if None in vals.values():
        raise RuntimeError(f'Missing primary metadata for {ev}: {vals}')
    if ev in event_meta and event_meta[ev] != vals:
        raise RuntimeError(f'Inconsistent duplicated event metadata for {ev}')
    event_meta[ev] = vals

events = sorted(event_meta)
feature_names = ['log_M_total_source', 'logit_q', 'chi_eff', 'redshift']
X = []
for ev in events:
    m = event_meta[ev]
    X.append([math.log(m['M_total_source']), logit(m['q']), m['chi_eff'], m['redshift']])
X = np.asarray(X, dtype=float)
mu = X.mean(axis=0)
S = np.cov(X, rowvar=False, ddof=1)
D = np.diag(np.diag(S))
C = (1.0 - SHRINKAGE_ALPHA) * S + SHRINKAGE_ALPHA * D
ridge = 0.0
score_type = 'MAHALANOBIS_SHRINKAGE'
score_status = 'OK'
score_warnings = []
try:
    eig = np.linalg.eigvalsh(C)
    cond = float(np.linalg.cond(C))
    if eig.min() <= 0 or not math.isfinite(cond) or cond > COND_MAX:
        raise np.linalg.LinAlgError(f'unstable covariance eig_min={eig.min()} cond={cond}')
    C_inv = np.linalg.inv(C)
    diffs = X - mu
    distances = np.sqrt(np.einsum('ij,jk,ik->i', diffs, C_inv, diffs))
except Exception as exc:
    score_type = 'FALLBACK_SCORE'
    score_status = 'FALLBACK_SCORE'
    score_warnings.append(str(exc))
    med = np.median(X, axis=0)
    mad = np.median(np.abs(X - med), axis=0)
    scale = np.where(mad > 0, 1.4826 * mad, np.std(X, axis=0, ddof=1))
    scale = np.where(scale > 0, scale, 1.0)
    distances = np.sqrt(np.sum(((X - med) / scale) ** 2, axis=1))
    eig = np.array([])
    cond = None

distance_by_event = {ev: float(distances[i]) for i, ev in enumerate(events)}
x_by_event = {ev: {feature_names[j]: float(X[i, j]) for j in range(len(feature_names))} for i, ev in enumerate(events)}

# ---------- add scores/ranks to row table ----------
for row in rows:
    ev = row['event']
    row['population_tail_distance'] = distance_by_event[ev]
    for fn, val in x_by_event[ev].items():
        row[fn] = val

# within-cohort ranks
by_cohort = defaultdict(list)
for row in rows:
    by_cohort[row['cohort']].append(row)
for cohort, group in by_cohort.items():
    rks = ranks_average([r['population_tail_distance'] for r in group])
    n = len(group)
    for row, rk in zip(group, rks):
        row['population_tail_rank'] = rk / n
        row['population_tail_top_tertile'] = (rk / n) >= TOP_TERTILE_THRESHOLD

# combined row-level ranks
combined_rks = ranks_average([r['population_tail_distance'] for r in rows])
for row, rk in zip(rows, combined_rks):
    row['population_tail_rank_combined'] = rk / len(rows)
    row['population_tail_top_tertile_combined'] = (rk / len(rows)) >= TOP_TERTILE_THRESHOLD
    row['score_type'] = score_type
    row['score_status'] = score_status
    row['score_basis_n_unique_events'] = len(events)

# ---------- statistical tests ----------
def analyze_group(label, group, rank_field='population_tail_rank'):
    x = [float(r[rank_field]) for r in group]
    y = [to_float(r['max_abs_residual']) for r in group]
    rho = spearman(x, y)
    p_perm, n_perm = perm_p_positive(x, y, rho)
    slope = theil_sen_slope(x, y)
    events_in_group = sorted({r['event'] for r in group})
    loo = []
    for ev in events_in_group:
        gg = [r for r in group if r['event'] != ev]
        if len(gg) < 4:
            continue
        xx = [float(r[rank_field]) for r in gg]
        yy = [to_float(r['max_abs_residual']) for r in gg]
        rr = spearman(xx, yy)
        ss = theil_sen_slope(xx, yy)
        loo.append({'left_out_event': ev, 'n': len(gg), 'spearman_rho': rr, 'theil_sen_slope': ss, 'delta_rho': rho - rr if math.isfinite(rho) and math.isfinite(rr) else None})
    if math.isfinite(rho) and rho > 0:
        stable = bool(loo) and all(x['spearman_rho'] > 0 for x in loo if math.isfinite(x['spearman_rho']))
    elif math.isfinite(rho) and rho < 0:
        stable = bool(loo) and all(x['spearman_rho'] < 0 for x in loo if math.isfinite(x['spearman_rho']))
    else:
        stable = False
    finite_loo = [x for x in loo if x.get('delta_rho') is not None and math.isfinite(x['delta_rho'])]
    influential = sorted(finite_loo, key=lambda d: abs(d['delta_rho']), reverse=True)[:5]
    sign_flips = [x for x in loo if math.isfinite(x['spearman_rho']) and math.isfinite(rho) and rho != 0 and np.sign(x['spearman_rho']) != np.sign(rho)]
    return {
        'group': label,
        'n_rows': len(group),
        'n_events': len(events_in_group),
        'rho': rho,
        'p_perm_positive': p_perm,
        'n_permutations': n_perm,
        'theil_sen_slope': slope,
        'loo_sign_stable': stable,
        'loo_min_rho': min((x['spearman_rho'] for x in loo if math.isfinite(x['spearman_rho'])), default=None),
        'loo_max_rho': max((x['spearman_rho'] for x in loo if math.isfinite(x['spearman_rho'])), default=None),
        'loo_sign_flip_events': [x['left_out_event'] for x in sign_flips],
        'top_influential_events': influential,
        'loo': loo,
    }

def analyze_predictor(label, group, predictor):
    pairs = []
    for r in group:
        xv = to_float(r[predictor])
        yv = to_float(r['max_abs_residual'])
        if xv is not None and yv is not None and math.isfinite(xv) and math.isfinite(yv):
            pairs.append((xv, yv, r['event']))
    x = [p[0] for p in pairs]
    y = [p[1] for p in pairs]
    rho = spearman(x, y) if len(pairs) >= 3 else float('nan')
    p_perm, n_perm = perm_p_positive(x, y, rho) if len(pairs) >= 4 else (None, 0)
    slope = theil_sen_slope(x, y) if len(pairs) >= 3 else float('nan')
    return {
        'group': label,
        'predictor': predictor,
        'n_rows': len(pairs),
        'n_events': len(set(p[2] for p in pairs)),
        'rho': rho,
        'p_perm_positive': p_perm,
        'n_permutations': n_perm,
        'theil_sen_slope': slope,
        'exploratory': True,
    }

primary_results = []
for cohort in sorted(by_cohort):
    primary_results.append(analyze_group(cohort, by_cohort[cohort], 'population_tail_rank'))
primary_results.append(analyze_group('COMBINED', rows, 'population_tail_rank_combined'))

# Combined unique-event diagnostic: average residual across duplicate cohorts. Not primary; used for dependence check.
unique_diag_rows = []
for ev in events:
    ev_rows = [r for r in rows if r['event'] == ev]
    rr = dict(ev_rows[0])
    rr['cohort'] = 'COMBINED_UNIQUE_EVENT_DIAGNOSTIC'
    rr['max_abs_residual'] = sum(to_float(r['max_abs_residual']) for r in ev_rows) / len(ev_rows)
    rr['verdict_kerr'] = 'marginal' if any(r['verdict_kerr'] == 'marginal' for r in ev_rows) else 'consistent'
    unique_diag_rows.append(rr)
unique_rks = ranks_average([r['population_tail_distance'] for r in unique_diag_rows])
for row, rk in zip(unique_diag_rows, unique_rks):
    row['population_tail_rank_combined'] = rk / len(unique_diag_rows)
combined_unique_result = analyze_group('COMBINED_UNIQUE_EVENT_DIAGNOSTIC', unique_diag_rows, 'population_tail_rank_combined')

# enrichment of marginal rows in top tertile
def enrichment(label, group, rank_field):
    n = len(group)
    top = [r for r in group if float(r[rank_field]) >= TOP_TERTILE_THRESHOLD]
    marg = [r for r in group if r['verdict_kerr'] == 'marginal']
    marg_top = [r for r in marg if float(r[rank_field]) >= TOP_TERTILE_THRESHOLD]
    top_frac = len(top) / n if n else float('nan')
    marg_frac = len(marg_top) / len(marg) if marg else None
    ratio = (marg_frac / top_frac) if marg and top_frac > 0 else None
    p_binom = binom_tail_geq(len(marg_top), len(marg), top_frac) if marg else None
    return {
        'group': label,
        'n_rows': n,
        'n_top_tertile': len(top),
        'top_tertile_fraction_all_rows': top_frac,
        'n_marginal': len(marg),
        'n_marginal_top_tertile': len(marg_top),
        'marginal_top_tertile_fraction': marg_frac,
        'enrichment_ratio_vs_all_rows': ratio,
        'binomial_p_geq_observed_given_top_fraction': p_binom,
        'marginal_events_top_tertile': sorted({r['event'] for r in marg_top}),
        'marginal_events_not_top_tertile': sorted({r['event'] for r in marg if r not in marg_top}),
    }

enrichment_results = []
for cohort in sorted(by_cohort):
    enrichment_results.append(enrichment(cohort, by_cohort[cohort], 'population_tail_rank'))
enrichment_results.append(enrichment('COMBINED', rows, 'population_tail_rank_combined'))

secondary_predictors = ['q', 'M_total_source', 'chi_eff', 'redshift', 'network_matched_filter_snr', 'p_astro', 'FAR']
secondary_results = []
for cohort in sorted(by_cohort):
    for pred in secondary_predictors:
        secondary_results.append(analyze_predictor(cohort, by_cohort[cohort], pred))
for pred in secondary_predictors:
    secondary_results.append(analyze_predictor('COMBINED', rows, pred))

# Criteria and final interpretation.
primary_by_group = {r['group']: r for r in primary_results}
enrich_by_group = {r['group']: r for r in enrichment_results}

def qualitative_group_signal(group):
    r = primary_by_group[group]
    e = enrich_by_group[group]
    return (
        math.isfinite(r['rho']) and r['rho'] > 0 and
        r['p_perm_positive'] is not None and r['p_perm_positive'] < 0.1 and
        r['loo_sign_stable'] and
        e['n_marginal'] > 0 and e['marginal_top_tertile_fraction'] is not None and e['marginal_top_tertile_fraction'] > e['top_tertile_fraction_all_rows']
    )

positive_groups = [g for g in ['T6.6_O3_literature', 'T8.2a_GWTC4_pSEOBNR'] if g in primary_by_group and qualitative_group_signal(g)]
combined_positive = qualitative_group_signal('COMBINED')
score_fallback = score_type == 'FALLBACK_SCORE'
# Unique-event dependence if a nominal positive group loses sign under LOO or only combined is positive.
depends_on_one_event = any(primary_by_group[g]['loo_sign_flip_events'] for g in positive_groups + (['COMBINED'] if combined_positive else []))
only_combined = combined_positive and not positive_groups

if score_fallback or depends_on_one_event or only_combined:
    interpretation = 'INCONCLUSIVE'
elif positive_groups and combined_positive:
    interpretation = 'POSITIVE'
elif positive_groups and not combined_positive:
    # User requires qualitative signal in T6.6 or T8.2a, not necessarily combined, but H1 is evaluated by group.
    interpretation = 'POSITIVE'
else:
    interpretation = 'NULL'

if interpretation == 'POSITIVE':
    recommendation = 'DO_CONTINUE'
elif interpretation == 'NULL':
    recommendation = 'KILL'
else:
    recommendation = 'PARK'

# Events influential across primary groups.
event_influence = defaultdict(lambda: {'max_abs_delta_rho': 0.0, 'groups': []})
for r in primary_results:
    for item in r['top_influential_events']:
        ev = item['left_out_event']
        delta = abs(item['delta_rho']) if item['delta_rho'] is not None else 0.0
        if delta > event_influence[ev]['max_abs_delta_rho']:
            event_influence[ev]['max_abs_delta_rho'] = delta
        event_influence[ev]['groups'].append({'group': r['group'], **item})
important_events = sorted(
    [{'event': ev, **data} for ev, data in event_influence.items()],
    key=lambda d: d['max_abs_delta_rho'],
    reverse=True,
)

# ---------- write row-level stats table ----------
new_fields = [
    'log_M_total_source', 'logit_q', 'population_tail_distance', 'population_tail_rank',
    'population_tail_rank_combined', 'population_tail_top_tertile', 'population_tail_top_tertile_combined',
    'score_type', 'score_status', 'score_basis_n_unique_events'
]
out_fields = [f for f in input_fields if f != '_row_id'] + [f for f in new_fields if f not in input_fields]
with OUT_CSV.open('w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=out_fields)
    w.writeheader()
    for row in rows:
        out = {}
        for field in out_fields:
            val = row.get(field, '')
            if isinstance(val, bool):
                val = 'true' if val else 'false'
            out[field] = val
        w.writerow(out)

# ---------- write JSON ----------
def clean(obj):
    if isinstance(obj, dict):
        return {k: clean(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [clean(v) for v in obj]
    if isinstance(obj, np.generic):
        return obj.item()
    if isinstance(obj, float):
        if math.isnan(obj) or math.isinf(obj):
            return None
        return obj
    return obj

summary = {
    'artifact': 'T9.2 population tail rank and residual association audit',
    'input_files': [str(INPUT), str(COVERAGE), str(NOTES_IN)],
    'output_files': [str(OUT_CSV), str(OUT_JSON), str(OUT_MD)],
    'n_rows': len(rows),
    'n_unique_events': len(events),
    'cohort_sizes': dict(Counter(r['cohort'] for r in rows)),
    'events_consulted_from_T9_1': coverage.get('events_consulted'),
    'chi_p_used': False,
    'primary_score': {
        'score_type': score_type,
        'score_status': score_status,
        'feature_vector': ['log(M_total_source)', 'logit(q)', 'chi_eff', 'redshift'],
        'estimated_on': 'unique events, duplicates not reweighted',
        'assigned_to': 'event x cohort rows',
        'shrinkage_alpha_to_diagonal': SHRINKAGE_ALPHA if score_type == 'MAHALANOBIS_SHRINKAGE' else None,
        'covariance_condition_number': cond,
        'covariance_eigenvalues': eig.tolist() if len(eig) else [],
        'warnings': score_warnings,
        'feature_mean': {feature_names[i]: float(mu[i]) for i in range(len(feature_names))},
        'covariance_matrix_regularized': C.tolist() if score_type == 'MAHALANOBIS_SHRINKAGE' else None,
    },
    'primary_h1_results': primary_results,
    'combined_unique_event_diagnostic': combined_unique_result,
    'marginal_top_tertile_enrichment': enrichment_results,
    'secondary_exploratory_results': secondary_results,
    'events_influential': important_events[:10],
    'decision_rules': {
        'positive': 'rho>0 with one-sided permutation p<0.1, positive leave-one-event-out sign stability, not one-event dependent, marginal enrichment in top tertile, and qualitative signal in T6.6 or T8.2a not only combined',
        'null': 'no signal meeting positive criteria',
        'inconclusive': 'score fallback, single-event dependence, or only combined signal',
    },
    'interpretation': interpretation,
    'recommendation': recommendation,
    'permutation_count_requested': PERMUTATIONS,
    'rng_seed': RNG_SEED,
}
OUT_JSON.write_text(json.dumps(clean(summary), indent=2, sort_keys=True) + '\n')

# ---------- write notes ----------
def fmt(x, nd=3):
    if x is None:
        return 'NA'
    try:
        if not math.isfinite(float(x)):
            return 'NA'
        return f'{float(x):.{nd}g}'
    except Exception:
        return str(x)

lines = []
lines.append('# T9.2 population tail rank vs Kerr residual')
lines.append('')
lines.append('- archivo: `population_tail_stats_table.csv`')
lines.append('- inputs reales: `population_metadata_table.csv`, `population_metadata_coverage.json`, `population_metadata_notes.md`.')
lines.append('- outputs reales: score poblacional, ranks por cohorte/combinado, tests H1 y secundarios exploratorios.')
lines.append('- funcion fisica: auditar si los residuos Kerr grandes se concentran en eventos poblacionalmente raros o en proxies de cobertura/seleccion de waveform.')
lines.append('- dependencia toy/teorica: ninguna nueva; no usa `chi_p`, no usa SNR/FAR/`p_astro` en el score primario.')
lines.append(f'- veredicto: {interpretation}; recomendacion: {recommendation}.')
lines.append('')
lines.append('## Score primario')
lines.append('')
lines.append(f'- Tipo: `{score_type}`.')
lines.append('- Vector: `log(M_total_source)`, `logit(q)`, `chi_eff`, `redshift`.')
lines.append('- Estimacion: 23 eventos unicos; duplicados entre cohortes no reponderan la covarianza.')
if score_type == 'MAHALANOBIS_SHRINKAGE':
    lines.append(f'- Covarianza regularizada: shrinkage diagonal alpha={SHRINKAGE_ALPHA}; condicion={fmt(cond,4)}.')
else:
    lines.append('- Covarianza no estable; se uso fallback robusto median/MAD. Esto fuerza lectura INCONCLUSIVE si apareciera senal.')
lines.append('')
lines.append('## H1 primaria')
lines.append('')
lines.append('| grupo | N filas | N eventos | rho Spearman | p_perm H1+ | Theil-Sen | LOO signo estable |')
lines.append('|---|---:|---:|---:|---:|---:|---|')
for r in primary_results:
    lines.append(f"| {r['group']} | {r['n_rows']} | {r['n_events']} | {fmt(r['rho'])} | {fmt(r['p_perm_positive'])} | {fmt(r['theil_sen_slope'])} | {str(r['loo_sign_stable']).lower()} |")
lines.append('')
lines.append('## Enrichment marginal / tercil alto')
lines.append('')
lines.append('| grupo | marginales en top tercil | marginales totales | fraccion marginal top | top tercil base | ratio |')
lines.append('|---|---:|---:|---:|---:|---:|')
for e in enrichment_results:
    lines.append(f"| {e['group']} | {e['n_marginal_top_tertile']} | {e['n_marginal']} | {fmt(e['marginal_top_tertile_fraction'])} | {fmt(e['top_tertile_fraction_all_rows'])} | {fmt(e['enrichment_ratio_vs_all_rows'])} |")
lines.append('')
lines.append('## Leave-one-out e influencia')
lines.append('')
for r in primary_results:
    infl = ', '.join(f"{x['left_out_event']} (d_rho={fmt(x['delta_rho'])})" for x in r['top_influential_events'][:3]) or 'NA'
    flips = ', '.join(r['loo_sign_flip_events']) or 'ninguno'
    lines.append(f"- `{r['group']}`: rho_LOO min={fmt(r['loo_min_rho'])}, max={fmt(r['loo_max_rho'])}; flips={flips}; influyentes={infl}.")
lines.append('')
lines.append('## Tests secundarios exploratorios')
lines.append('')
lines.append('| grupo | predictor | rho | p_perm H1+ | Theil-Sen |')
lines.append('|---|---|---:|---:|---:|')
for s in secondary_results:
    lines.append(f"| {s['group']} | {s['predictor']} | {fmt(s['rho'])} | {fmt(s['p_perm_positive'])} | {fmt(s['theil_sen_slope'])} |")
lines.append('')
lines.append('## Diagnostico combinado unico')
lines.append('')
lines.append(f"- Combinado por evento unico, promediando residuos de eventos duplicados: rho={fmt(combined_unique_result['rho'])}, p_perm={fmt(combined_unique_result['p_perm_positive'])}, slope={fmt(combined_unique_result['theil_sen_slope'])}.")
lines.append('- Este diagnostico no sustituye los tests por cohorte; sirve para detectar dependencia de duplicados entre cohortes.')
lines.append('')
lines.append('## Interpretacion')
lines.append('')
if interpretation == 'NULL':
    lines.append('- No hay asociacion positiva que cumpla simultaneamente p_perm<0.1, estabilidad leave-one-out, enriquecimiento de marginales y senal cualitativa por cohorte.')
    lines.append('- Resultado estadistico: NULL para T9.2. Esto no es una refutacion fisica global; solo dice que esta muestra no soporta la hipotesis population-tail.')
elif interpretation == 'POSITIVE':
    lines.append('- Hay una senal positiva que pasa los criterios operativos definidos para T9.2. Debe tratarse como exploratoria por N pequeno.')
else:
    lines.append('- La lectura queda INCONCLUSIVE por dependencia operacional indicada en el JSON o por score fallback.')
lines.append(f'- Recomendacion: `{recommendation}`.')
lines.append('')
lines.append('## Guardrails')
lines.append('')
lines.append('- No se modifico YAML canonico, codigo principal, thresholds ni stages 02/03/04.')
lines.append('- No se consultaron nuevas fuentes.')
lines.append('- `chi_p` queda aparcado por cobertura 0/23.')
lines.append('- SNR/FAR/`p_astro` aparecen solo como tests secundarios exploratorios, no en el score primario.')
OUT_MD.write_text('\n'.join(lines) + '\n')

print(json.dumps(clean({
    'score_type': score_type,
    'cond': cond,
    'interpretation': interpretation,
    'recommendation': recommendation,
    'primary_h1': [{k:r[k] for k in ['group','n_rows','n_events','rho','p_perm_positive','theil_sen_slope','loo_sign_stable','loo_min_rho','loo_max_rho','loo_sign_flip_events']} for r in primary_results],
    'enrichment': enrichment_results,
    'top_influential': important_events[:5],
    'outputs': [str(OUT_CSV), str(OUT_JSON), str(OUT_MD)]
}), indent=2))
