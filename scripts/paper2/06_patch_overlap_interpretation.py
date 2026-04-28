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
md=base/'snr_overlap_decomposition_notes.md'
js=base/'snr_overlap_decomposition_summary.json'
text=md.read_text()
text=text.replace(
'- `GW190828_063405` y `GW190910_112807` no mejoran: T8.2a mantiene o sube `max_abs_residual`, con maximo dominado por gamma. No hay desaparicion universal de residuo en pSEOBNRv5PHM.',
'- `GW190828_063405` y `GW190910_112807` no mejoran: T8.2a mantiene o sube `max_abs_residual`. En `GW190828_063405` el maximo pasa a frecuencia; en `GW190910_112807` queda dominado por gamma. No hay desaparicion universal de residuo en pSEOBNRv5PHM.'
)
md.write_text(text)
d=json.loads(js.read_text())
d['limited_interpretation']['not_universal']='GW190828_063405 and GW190910_112807 do not improve in T8.2a; GW190828_063405 becomes frequency-dominated, while GW190910_112807 remains gamma/damping-dominated. There is no universal residual-tail disappearance in pSEOBNRv5PHM.'
js.write_text(json.dumps(d, indent=2, sort_keys=True)+'\n')
print('corrected non-improvement component description')
