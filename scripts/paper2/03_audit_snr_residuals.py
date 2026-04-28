"""
Paper 2 analysis producer.

This script is part of the reproducibility snapshot for the Paper 2 analysis.
It operates on frozen input tables and writes the corresponding verified
analysis outputs. External catalog metadata should be frozen before downstream
statistical analyses.
"""
import csv, json, math, random, statistics
from pathlib import Path
from collections import Counter, defaultdict
import numpy as np

IN_DIR = Path('runs_sync/active/kerr_population_tail_t9')
OUT_DIR = Path('runs_sync/active/kerr_snr_systematics_t10')
OUT_DIR.mkdir(parents=True, exist_ok=True)
IN_CSV = IN_DIR / 'population_tail_stats_table.csv'
IN_JSON = IN_DIR / 'population_tail_summary.json'
OUT_CSV = OUT_DIR / 'snr_residual_audit_table.csv'
OUT_JSON = OUT_DIR / 'snr_residual_summary.json'
OUT_MD = OUT_DIR / 'snr_residual_notes.md'

N_PERM = 20000
SEED = 10010
TOPK = [1, 2, 3]


def ffloat(x):
    if x is None or x == '':
        return None
    return float(x)


def ranks_average(values):
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
    return pearson(ranks_average(x), ranks_average(y))


def perm_p_positive(x, y, obs, n_perm=N_PERM, seed=SEED):
    if len(x) < 4 or not math.isfinite(obs):
        return None, 0
    rng = random.Random(seed + len(x) * 7919 + int(sum(ranks_average(x)) * 17))
    yy = list(y)
    count = 0
    for _ in range(n_perm):
        yp = yy[:]
        rng.shuffle(yp)
        rr = spearman(x, yp)
        if math.isfinite(rr) and rr >= obs:
            count += 1
    return (count + 1) / (n_perm + 1), n_perm


def ols_residual(y, X):
    y = np.asarray(y, dtype=float)
    X = np.asarray(X, dtype=float)
    if X.ndim == 1:
        X = X.reshape(-1, 1)
    X = np.column_stack([np.ones(len(y)), X])
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    return y - X @ beta


def partial_spearman(x, y, controls):
    if len(x) < 5:
        return float('nan')
    rx = np.asarray(ranks_average(x), dtype=float)
    ry = np.asarray(ranks_average(y), dtype=float)
    C = np.column_stack([ranks_average(c) for c in controls]) if controls else np.zeros((len(x), 0))
    if C.shape[1] == 0:
        return pearson(rx, ry)
    try:
        ex = ols_residual(rx, C)
        ey = ols_residual(ry, C)
        return pearson(ex, ey)
    except Exception:
        return float('nan')


def partial_perm_p_positive(x, y, controls, obs, n_perm=N_PERM, seed=SEED):
    if len(x) < 6 or not math.isfinite(obs):
        return None, 0
    rng = random.Random(seed + len(x) * 1237 + len(controls) * 31)
    yy = list(y)
    count = 0
    for _ in range(n_perm):
        yp = yy[:]
        rng.shuffle(yp)
        rr = partial_spearman(x, yp, controls)
        if math.isfinite(rr) and rr >= obs:
            count += 1
    return (count + 1) / (n_perm + 1), n_perm


def theil_sen_slope(x, y):
    slopes=[]
    for i in range(len(x)):
        for j in range(i+1, len(x)):
            dx=x[j]-x[i]
            if dx != 0:
                slopes.append((y[j]-y[i])/dx)
    return float(statistics.median(slopes)) if slopes else float('nan')


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

with IN_CSV.open(newline='') as f:
    reader = csv.DictReader(f)
    rows = list(reader)
    input_fields = reader.fieldnames or []
for i, r in enumerate(rows):
    r['_row_id'] = i
    r['_snr'] = ffloat(r['network_matched_filter_snr'])
    r['_resid'] = ffloat(r['max_abs_residual'])
    r['_M'] = ffloat(r['M_total_source'])
    r['_q'] = ffloat(r['q'])
    r['_z'] = ffloat(r['redshift'])
    r['_rank_within'] = ffloat(r['population_tail_rank'])
    r['_rank_combined'] = ffloat(r['population_tail_rank_combined'])

with IN_JSON.open() as f:
    t9 = json.load(f)

cohorts = sorted({r['cohort'] for r in rows})
groups = {c: [r for r in rows if r['cohort'] == c] for c in cohorts}
groups['COMBINED'] = list(rows)

# Rank tables requested: rank by SNR and by max_abs_residual inside cohort and combined.
for label, group in groups.items():
    snr_order = sorted(group, key=lambda r: (-r['_snr'], r['event'], r['cohort']))
    res_order = sorted(group, key=lambda r: (-r['_resid'], r['event'], r['cohort']))
    n=len(group)
    field_prefix = 'combined' if label == 'COMBINED' else 'cohort'
    for pos, r in enumerate(snr_order, 1):
        if label == 'COMBINED':
            r['snr_rank_combined_desc'] = pos
            r['snr_percentile_combined_desc'] = pos / n
        else:
            r['snr_rank_cohort_desc'] = pos
            r['snr_percentile_cohort_desc'] = pos / n
    for pos, r in enumerate(res_order, 1):
        if label == 'COMBINED':
            r['residual_rank_combined_desc'] = pos
            r['residual_percentile_combined_desc'] = pos / n
        else:
            r['residual_rank_cohort_desc'] = pos
            r['residual_percentile_cohort_desc'] = pos / n


def corr_result(label, group):
    x=[r['_snr'] for r in group]
    y=[r['_resid'] for r in group]
    rho=spearman(x,y)
    p,nperm=perm_p_positive(x,y,rho)
    slope=theil_sen_slope(x,y)
    return {
        'group': label,
        'n_rows': len(group),
        'n_events': len({r['event'] for r in group}),
        'spearman_rho': rho,
        'p_perm_positive': p,
        'n_permutations': nperm,
        'theil_sen_slope': slope,
    }

primary=[]
for label, group in groups.items():
    primary.append(corr_result(label, group))
primary_by_group={r['group']:r for r in primary}

# Leave-one-out by event.
loo=[]
for label, group in groups.items():
    base=primary_by_group[label]
    for ev in sorted({r['event'] for r in group}):
        gg=[r for r in group if r['event'] != ev]
        if len(gg) < 4:
            continue
        cr=corr_result(label, gg)
        loo.append({
            'group': label,
            'left_out_event': ev,
            'n_rows': len(gg),
            'n_events': len({r['event'] for r in gg}),
            'spearman_rho': cr['spearman_rho'],
            'p_perm_positive': cr['p_perm_positive'],
            'theil_sen_slope': cr['theil_sen_slope'],
            'delta_rho': base['spearman_rho'] - cr['spearman_rho'] if math.isfinite(base['spearman_rho']) and math.isfinite(cr['spearman_rho']) else None,
            'sign_flip': bool(math.isfinite(base['spearman_rho']) and math.isfinite(cr['spearman_rho']) and base['spearman_rho'] != 0 and np.sign(base['spearman_rho']) != np.sign(cr['spearman_rho'])),
        })

loo_summary={}
for label in groups:
    vals=[x for x in loo if x['group']==label and x['spearman_rho'] is not None]
    finite=[x for x in vals if math.isfinite(x['spearman_rho'])]
    sig=[x for x in finite if x['p_perm_positive'] is not None and x['p_perm_positive'] < 0.1 and x['spearman_rho'] > 0]
    loo_summary[label]={
        'n_leave_one_event_runs': len(finite),
        'min_rho': min((x['spearman_rho'] for x in finite), default=None),
        'max_rho': max((x['spearman_rho'] for x in finite), default=None),
        'all_positive': all(x['spearman_rho'] > 0 for x in finite) if finite else False,
        'all_p_lt_0_1_positive': len(sig) == len(finite) if finite else False,
        'n_p_lt_0_1_positive': len(sig),
        'sign_flip_events': [x['left_out_event'] for x in finite if x['sign_flip']],
        'top_influential': sorted(finite, key=lambda d: abs(d['delta_rho']) if d['delta_rho'] is not None else -1, reverse=True)[:8],
    }

# Top-SNR jackknife: remove events, not rows. Tie handled by event max SNR then event name.
topk_results=[]
for label, group in groups.items():
    event_max=[]
    for ev in sorted({r['event'] for r in group}):
        event_rows=[r for r in group if r['event']==ev]
        event_max.append((max(r['_snr'] for r in event_rows), ev))
    event_order=[ev for snr,ev in sorted(event_max, key=lambda t:(-t[0], t[1]))]
    for k in TOPK:
        removed=event_order[:k]
        gg=[r for r in group if r['event'] not in removed]
        cr=corr_result(label, gg) if len(gg) >= 4 else {'spearman_rho': None, 'p_perm_positive': None, 'theil_sen_slope': None, 'n_rows': len(gg), 'n_events': len({r['event'] for r in gg}), 'n_permutations': 0}
        topk_results.append({
            'group': label,
            'k': k,
            'removed_events': removed,
            'n_rows': len(gg),
            'n_events': len({r['event'] for r in gg}),
            'spearman_rho': cr['spearman_rho'],
            'p_perm_positive': cr['p_perm_positive'],
            'theil_sen_slope': cr['theil_sen_slope'],
        })

# Partial Spearman controls.
control_specs = {
    'population_tail_rank': lambda label, r: r['_rank_combined'] if label == 'COMBINED' else r['_rank_within'],
    'M_total_source': lambda label, r: r['_M'],
    'q': lambda label, r: r['_q'],
    'redshift': lambda label, r: r['_z'],
}
partial_results=[]
for label, group in groups.items():
    x=[r['_snr'] for r in group]
    y=[r['_resid'] for r in group]
    for cname, getter in control_specs.items():
        controls=[[getter(label, r) for r in group]]
        rho=partial_spearman(x,y,controls)
        p,nperm=partial_perm_p_positive(x,y,controls,rho)
        partial_results.append({
            'group': label,
            'control': cname,
            'n_rows': len(group),
            'n_events': len({r['event'] for r in group}),
            'partial_spearman_rho': rho,
            'p_perm_positive': p,
            'n_permutations': nperm,
        })
    controls=[[getter(label, r) for r in group] for getter in control_specs.values()]
    rho=partial_spearman(x,y,controls)
    p,nperm=partial_perm_p_positive(x,y,controls,rho)
    partial_results.append({
        'group': label,
        'control': 'population_tail_rank+M_total_source+q+redshift',
        'n_rows': len(group),
        'n_events': len({r['event'] for r in group}),
        'partial_spearman_rho': rho,
        'p_perm_positive': p,
        'n_permutations': nperm,
    })

# Attach row flags for audit table.
primary_labels=[]
for r in rows:
    flags=[]
    if r['snr_rank_cohort_desc'] <= 3:
        flags.append('TOP3_SNR_COHORT')
    if r['residual_rank_cohort_desc'] <= 3:
        flags.append('TOP3_RESIDUAL_COHORT')
    if r['snr_rank_combined_desc'] <= 5:
        flags.append('TOP5_SNR_COMBINED')
    if r['residual_rank_combined_desc'] <= 5:
        flags.append('TOP5_RESIDUAL_COMBINED')
    r['audit_flags'] = ';'.join(flags)

# Interpretation criteria.
def survives_primary(label):
    r=primary_by_group[label]
    return r['spearman_rho'] is not None and r['spearman_rho'] > 0 and r['p_perm_positive'] is not None and r['p_perm_positive'] < 0.1

def survives_loo(label):
    s=loo_summary[label]
    return s['all_positive'] and s['all_p_lt_0_1_positive'] and not s['sign_flip_events']

def survives_topk(label):
    vals=[x for x in topk_results if x['group']==label]
    return all(x['spearman_rho'] is not None and x['spearman_rho'] > 0 and x['p_perm_positive'] is not None and x['p_perm_positive'] < 0.1 for x in vals)

def survives_controls(label):
    vals=[x for x in partial_results if x['group']==label]
    return all(x['partial_spearman_rho'] is not None and x['partial_spearman_rho'] > 0 and x['p_perm_positive'] is not None and x['p_perm_positive'] < 0.1 for x in vals)

robust_groups=[]
event_driven_groups=[]
null_groups=[]
inconclusive_groups=[]
for label in groups:
    if not survives_primary(label):
        null_groups.append(label)
        continue
    loo_ok=survives_loo(label)
    topk_ok=survives_topk(label)
    ctrl_ok=survives_controls(label)
    if loo_ok and topk_ok and ctrl_ok:
        robust_groups.append(label)
    elif not loo_ok or not topk_ok:
        event_driven_groups.append(label)
    else:
        inconclusive_groups.append(label)

# Overall: robust diagnostic requires T6.6 and combined survival, not T8-only. If primary exists but fails event jackknife => event-driven.
if robust_groups and ('T6.6_O3_literature' in robust_groups or 'COMBINED' in robust_groups):
    interpretation='ROBUST_DIAGNOSTIC'
elif event_driven_groups:
    interpretation='EVENT_DRIVEN'
elif inconclusive_groups:
    interpretation='INCONCLUSIVE'
else:
    interpretation='NULL'

recommendation = {'ROBUST_DIAGNOSTIC':'DO_CONTINUE', 'EVENT_DRIVEN':'PARK', 'INCONCLUSIVE':'PARK', 'NULL':'KILL'}[interpretation]

# Write audit table.
fields = [
    'cohort','event','verdict_kerr','max_abs_residual','network_matched_filter_snr',
    'snr_rank_cohort_desc','snr_percentile_cohort_desc','snr_rank_combined_desc','snr_percentile_combined_desc',
    'residual_rank_cohort_desc','residual_percentile_cohort_desc','residual_rank_combined_desc','residual_percentile_combined_desc',
    'population_tail_rank','population_tail_rank_combined','M_total_source','q','redshift','audit_flags'
]
with OUT_CSV.open('w', newline='') as f:
    w=csv.DictWriter(f, fieldnames=fields)
    w.writeheader()
    for r in sorted(rows, key=lambda rr:(rr['cohort'], int(rr['snr_rank_cohort_desc']), int(rr['residual_rank_cohort_desc']))):
        out={}
        for field in fields:
            val=r.get(field,'')
            out[field]=val
        w.writerow(out)

summary={
    'artifact':'T10.0 SNR residual robustness audit',
    'input_files':[str(IN_CSV), str(IN_JSON)],
    'output_files':[str(OUT_CSV), str(OUT_JSON), str(OUT_MD)],
    'n_rows':len(rows),
    'n_unique_events':len({r['event'] for r in rows}),
    'cohort_sizes':dict(Counter(r['cohort'] for r in rows)),
    'method':{
        'primary_association':'Spearman(max_abs_residual, network_matched_filter_snr)',
        'permutation_p':'one-sided positive, random label permutations, deterministic seed',
        'n_permutations':N_PERM,
        'leave_one_out':'event-level removal; combined removes all rows for a duplicated event',
        'top_snr_jackknife':'event-level removal of top 1, top 2, top 3 events by max SNR within group',
        'partial_control':'partial Spearman: residualized ranks with OLS controls, with permutation p-values',
        'controls':['population_tail_rank within group or combined rank','M_total_source','q','redshift','joint all four'],
    },
    'primary_spearman':primary,
    'leave_one_out_summary':loo_summary,
    'leave_one_out_runs':loo,
    'top_snr_jackknife':topk_results,
    'partial_control_results':partial_results,
    'groups_surviving':{
        'primary': [g for g in groups if survives_primary(g)],
        'leave_one_out': [g for g in groups if survives_primary(g) and survives_loo(g)],
        'top_snr_jackknife': [g for g in groups if survives_primary(g) and survives_topk(g)],
        'controls': [g for g in groups if survives_primary(g) and survives_controls(g)],
        'robust': robust_groups,
        'event_driven': event_driven_groups,
        'null': null_groups,
        'inconclusive': inconclusive_groups,
    },
    'events_that_drive_correlation':{
        g: loo_summary[g]['top_influential'][:5] for g in groups
    },
    'top_snr_events_by_group':{
        g: [
            {'event': ev, 'max_snr': snr}
            for snr, ev in sorted([(max(r['_snr'] for r in group if r['event']==ev), ev) for ev in sorted({r['event'] for r in group})], key=lambda t:(-t[0], t[1]))[:5]
        ] for g, group in groups.items()
    },
    'interpretation': interpretation,
    'recommendation': recommendation,
    'rng_seed': SEED,
}
OUT_JSON.write_text(json.dumps(clean(summary), indent=2, sort_keys=True) + '\n')

# Notes.
def fmt(x, nd=3):
    if x is None:
        return 'NA'
    try:
        x=float(x)
        if not math.isfinite(x): return 'NA'
        return f'{x:.{nd}g}'
    except Exception:
        return str(x)

lines=[]
lines.append('# T10.0 SNR residual robustness audit')
lines.append('')
lines.append('- archivo: `snr_residual_audit_table.csv`')
lines.append('- inputs reales: `population_tail_stats_table.csv`, `population_tail_summary.json`.')
lines.append('- outputs reales: ranking por SNR/residuo, Spearman, permutation p-value, leave-one-out, top-SNR jackknife y controles parciales.')
lines.append('- funcion fisica: auditar si la senal secundaria SNR-residuo es robusta o un artefacto de pocos eventos/proxies poblacionales.')
lines.append('- dependencia toy/teorica: ninguna nueva; no se ejecutan stages ni se consultan fuentes externas.')
lines.append(f'- veredicto: {interpretation}; recomendacion: {recommendation}.')
lines.append('')
lines.append('## Asociacion primaria SNR-residuo')
lines.append('')
lines.append('| grupo | N filas | N eventos | rho | p_perm H1+ | Theil-Sen |')
lines.append('|---|---:|---:|---:|---:|---:|')
for r in primary:
    lines.append(f"| {r['group']} | {r['n_rows']} | {r['n_events']} | {fmt(r['spearman_rho'])} | {fmt(r['p_perm_positive'])} | {fmt(r['theil_sen_slope'])} |")
lines.append('')
lines.append('## Leave-one-out')
lines.append('')
lines.append('| grupo | rho min | rho max | runs p<0.1 positivo | sign flips | eventos mas influyentes |')
lines.append('|---|---:|---:|---:|---|---|')
for g in groups:
    s=loo_summary[g]
    infl=', '.join(f"{x['left_out_event']} (d={fmt(x['delta_rho'])})" for x in s['top_influential'][:3]) or 'NA'
    flips=', '.join(s['sign_flip_events']) or 'ninguno'
    lines.append(f"| {g} | {fmt(s['min_rho'])} | {fmt(s['max_rho'])} | {s['n_p_lt_0_1_positive']}/{s['n_leave_one_event_runs']} | {flips} | {infl} |")
lines.append('')
lines.append('## Jackknife top-SNR')
lines.append('')
lines.append('| grupo | quita | eventos quitados | rho | p_perm H1+ |')
lines.append('|---|---:|---|---:|---:|')
for r in topk_results:
    lines.append(f"| {r['group']} | top {r['k']} | {', '.join(r['removed_events'])} | {fmt(r['spearman_rho'])} | {fmt(r['p_perm_positive'])} |")
lines.append('')
lines.append('## Control parcial')
lines.append('')
lines.append('| grupo | control | partial rho | p_perm H1+ |')
lines.append('|---|---|---:|---:|')
for r in partial_results:
    lines.append(f"| {r['group']} | {r['control']} | {fmt(r['partial_spearman_rho'])} | {fmt(r['p_perm_positive'])} |")
lines.append('')
lines.append('## Eventos que impulsan la correlacion')
lines.append('')
for g in groups:
    tops=loo_summary[g]['top_influential'][:5]
    s=', '.join(f"{x['left_out_event']} (delta_rho={fmt(x['delta_rho'])}, rho_sin={fmt(x['spearman_rho'])}, p_sin={fmt(x['p_perm_positive'])})" for x in tops)
    lines.append(f'- `{g}`: {s}')
lines.append('')
lines.append('## Interpretacion')
lines.append('')
if interpretation == 'ROBUST_DIAGNOSTIC':
    lines.append('- La asociacion SNR-residuo sobrevive leave-one-out, top-SNR jackknife y controles parciales en al menos el grupo operativo relevante.')
elif interpretation == 'EVENT_DRIVEN':
    lines.append('- Hay asociacion primaria en algun grupo, pero se degrada al quitar eventos de alto SNR o eventos influyentes. No debe venderse como diagnostico robusto.')
elif interpretation == 'NULL':
    lines.append('- No hay asociacion primaria positiva suficiente en los grupos auditados.')
else:
    lines.append('- La asociacion no queda resuelta con robustez suficiente para decidir entre diagnostico y artefacto.')
lines.append(f'- Recomendacion: `{recommendation}`.')
lines.append('')
lines.append('## Guardrails')
lines.append('')
lines.append('- No se modifico YAML, codigo principal ni thresholds.')
lines.append('- No se ejecuto Stage 02/03/04.')
lines.append('- No se consultaron nuevas fuentes.')
lines.append('- No se construye narrativa fisica; esto es auditoria tecnica/estadistica de una correlacion secundaria.')
OUT_MD.write_text('\n'.join(lines) + '\n')

print(json.dumps(clean({
    'interpretation': interpretation,
    'recommendation': recommendation,
    'primary': primary,
    'loo_summary': loo_summary,
    'top_snr_jackknife': topk_results,
    'partial_control_results': partial_results,
    'groups_surviving': summary['groups_surviving'],
    'outputs': [str(OUT_CSV), str(OUT_JSON), str(OUT_MD)]
}), indent=2))
