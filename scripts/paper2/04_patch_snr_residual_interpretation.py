"""
Paper 2 analysis producer.

This script is part of the reproducibility snapshot for the Paper 2 analysis.
It operates on frozen input tables and writes the corresponding verified
analysis outputs. External catalog metadata should be frozen before downstream
statistical analyses.
"""
import json
from pathlib import Path
base=Path('runs_sync/active/kerr_snr_systematics_t10')
js=base/'snr_residual_summary.json'
md=base/'snr_residual_notes.md'
d=json.loads(js.read_text())
d['interpretation_scope']={
    'ROBUST_DIAGNOSTIC_scope':'T6.6_O3_literature only',
    'T8.2a_GWTC4_pSEOBNR':'NULL: primary SNR-residual association is positive but not significant and does not survive controls.',
    'COMBINED':'EVENT_DRIVEN_OR_CONTROL_FRAGILE: primary association is positive and top-k survives, but not all LOO p-values remain <0.1 and joint population controls remove the signal.',
    'do_not_read_as':'global physical claim across cohorts',
}
js.write_text(json.dumps(d, indent=2, sort_keys=True)+'\n')
text=md.read_text()
old='''## Interpretacion\n\n- La asociacion SNR-residuo sobrevive leave-one-out, top-SNR jackknife y controles parciales en al menos el grupo operativo relevante.\n- Recomendacion: `DO_CONTINUE`.'''
new='''## Interpretacion\n\n- `ROBUST_DIAGNOSTIC` aplica estrictamente a `T6.6_O3_literature`: sobrevive leave-one-out, top-SNR jackknife y controles parciales, incluido el control conjunto.\n- `T8.2a_GWTC4_pSEOBNR` queda NULL: rho positivo pero p_perm no significativo y controles parciales no sostienen la senal.\n- `COMBINED` es fragil a controles: top-SNR jackknife conserva p<0.1, pero el control conjunto `population_tail_rank+M_total_source+q+redshift` deja rho=0.146 y p=0.239.\n- No leer esto como claim fisico global entre cohortes; es un diagnostico tecnico de SNR en T6.6.\n- Recomendacion: `DO_CONTINUE` solo para auditoria de sistematicos/cobertura SNR, no para narrativa fisica.'''
if old not in text:
    raise SystemExit('expected block not found')
md.write_text(text.replace(old,new))
print('updated interpretation_scope')
