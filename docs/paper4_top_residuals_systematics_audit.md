# Paper 4 — Top Residuals Systematics Audit

## Scope

This note audits obvious input and convention systematics for the largest descriptive 220 Kerr residuals. It does not identify physical cases for follow-up, does not change residuals, does not recalculate Kerr predictions, and does not introduce new thresholds.

## Input

- descriptive table: `runs/paper4_residual_audit_v1/paper4_220_residuals_descriptive.csv`
- schema-aligned dataset: `runs/paper4_qnm_dataset_schema_v2_renamed/qnm_dataset_220.csv`
- YAML source: `data/phase1_data/qnm_events_literature.yml`

## Top residual events

| event_id | mode | redshift | residual_f | residual_gamma | max_abs_residual | source_paper |
|---|---:|---:|---:|---:|---:|---|
| GW150914 | 220 | 0.090 | 0.863 | 1.683 | 1.683 | Tests of General Relativity with Binary Black Holes from the second LIGO-Virgo Gravitational-Wave Transient Catalog |
| GW190708_232457 | 220 | 0.197 | 1.010 | 1.569 | 1.569 | Tests of General Relativity with Binary Black Holes from the second LIGO-Virgo Gravitational-Wave Transient Catalog |
| GW170814 | 220 | 0.124 | 0.776 | 1.515 | 1.515 | Tests of General Relativity with Binary Black Holes from the second LIGO-Virgo Gravitational-Wave Transient Catalog |
| GW190521_074359 | 220 | 0.210 | 0.645 | 1.324 | 1.324 | Tests of General Relativity with Binary Black Holes from the second LIGO-Virgo Gravitational-Wave Transient Catalog |
| GW170104 | 220 | 0.200 | 0.521 | 1.015 | 1.015 | Tests of General Relativity with Binary Black Holes from the second LIGO-Virgo Gravitational-Wave Transient Catalog |

## Systematic checks

Redshift wording is descriptive for this audit: GW150914 is low-redshift relative to this subset, while the other four top rows are moderate-redshift rows. No high-redshift row appears in the top five.

| event_id | redshift level | sigma_M_final_Msun missing? | sigma_chi_final missing? | sigma_tau_ms present? | source/provenance clear? | dominant residual | preliminary interpretation | comment |
|---|---|---|---|---|---|---|---|---|
| GW150914 | low | no | no | yes | yes; `source_paper` and `pole_source` agree | gamma | not_explained_by_schema_only; convention_check_needed | Metadata and propagated mass/spin uncertainty fields are present. The largest residual is damping-side, so damping-time/gamma conventions and source table interpretation should be checked before further classification. |
| GW190708_232457 | moderate | no | no | yes | yes; `source_paper` and `pole_source` agree | gamma | not_explained_by_schema_only; convention_check_needed | Frequency and damping residuals are both among the larger rows, but damping is larger. Redshift is present, not missing, so this is not explained by schema absence alone. |
| GW170814 | moderate | no | no | yes | yes; `source_paper` and `pole_source` agree | gamma | not_explained_by_schema_only; convention_check_needed | All required uncertainty fields inspected here are populated. The residual ranking is again damping-dominated. |
| GW190521_074359 | moderate | no | no | yes | yes; `source_paper` and `pole_source` agree | gamma | not_explained_by_schema_only; convention_check_needed | Redshift and final-state uncertainties are present. The remaining obvious check is convention/source-systematics, especially for damping. |
| GW170104 | moderate | no | no | yes | yes; `source_paper` and `pole_source` agree | gamma | not_explained_by_schema_only; convention_check_needed | This row has the smallest top-five `max_abs_residual`; metadata inspected here is complete, and the larger component is still `residual_gamma`. |

## Preliminary interpretation

The top-five rows do not appear to be dominated by missing schema fields: `z`, `M_final_Msun`, `sigma_M_final_Msun`, `chi_final`, `sigma_chi_final`, `sigma_tau_ms`, `source_paper`, and `pole_source` are populated for all five rows. The obvious residual pattern is damping-side dominance, so convention_check_needed is the common preliminary label.

The single-source provenance is clear but still narrow: all five rows cite the same `source_paper`. That leaves input_dominated_possible as a useful caution until source-table conventions and systematic assumptions are audited.

## Immediate conclusion

The largest descriptive residuals are not ready for preliminary classification from this table alone. They first need a focused audit of source conventions, damping-time/gamma handling, and uncertainty propagation assumptions.

## Next step

Audit damping convention and source-table provenance for the five highest-residual rows.
