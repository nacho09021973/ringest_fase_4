# Paper 4 — Posterior Samples Availability Inventory

## Scope

This document inventories possible posterior-sample sources for resolving the strong remnant median mapping criticism in Paper 4. It does not download data, inspect external releases, create scripts, modify CSV files, generate runs, or make candidate claims.

The inventory is deliberately conservative. A source is not treated as available for Level 2 until concrete files, event coverage, parameter names, and provenance are verified.

## Level 2 requirement

The strong remnant mapping question is whether the current point-median comparison

```text
f_Kerr(median(M_final), median(chi_final))
```

differs materially from the posterior-propagated quantity

```text
median(f_Kerr(M_final, chi_final)).
```

Resolving this requires joint posterior samples for `M_final` and `chi_final` per event. Ideally, the same audit would also identify whether posterior information exists for observed ringdown frequency and damping quantities, such as `f_220`, `freq`, `tau`, or related QNM parameters, but the minimum Level 2 gate is the joint remnant posterior.

## Source families

### GWOSC / LVK parameter-estimation releases

GWOSC/LVK parameter-estimation releases are the most plausible source for remnant mass and remnant spin posterior samples. These products are usually organized by event and waveform/PE run, but this repository has not yet verified concrete posterior files for the Paper 4 event set.

Fields to search for, without assuming exact names:

- final mass fields: `final_mass`, `remnant_mass`, `M_final`, `final_mass_source`;
- final spin fields: `final_spin`, `remnant_spin`, `chi_final`;
- cosmology/redshift fields if detector/source-frame conversions are needed: `redshift`, `luminosity_distance`;
- component masses and spins useful for provenance and secondary checks: `mass_1_source`, `mass_2_source`, aligned spin fields, in-plane spin fields, effective spin, precession fields.

These samples would address the core Level 2 remnant-mapping issue if they include joint event-level samples for `M_final` and `chi_final` with known source/detector-frame convention.

### GWTC-2 TGR / O3a TGR products

The phase1 Paper 4 input is based on GWTC-2 TGR IMR tabulated ringdown quantities. Local repository evidence points to the current inputs being summaries, not posterior samples: the active CSVs contain scalar values such as `freq_hz`, `tau_ms`, `M_final_Msun`, `chi_final`, their scalar uncertainties, `f_kerr_hz`, and `residual_f`.

GWTC-2/O3a TGR-associated products may have ringdown or agnostic analyses, potentially including pyRing-style outputs or posteriors for frequency and damping quantities. That availability has not been verified in this repository. If present, such products could help audit observed-side `f_220`/`tau` posteriors separately from remnant mass/spin posteriors.

For Level 2 remnant mapping, the essential requirement remains joint samples of `M_final` and `chi_final` for the same event/run provenance used by the tabulated Paper 4 inputs.

### GWTC-4 pSEOBNR source

The current GWTC-4 pSEOBNR Paper 4 input appears to be a table/summary-derived source: the local CSV contains scalar remnant values, scalar uncertainties, observed frequency/damping summaries, and derived residual columns. It does not itself contain posterior samples.

A separate release would be needed to obtain posterior samples matching the GWTC-4 pSEOBNR source. Availability should not be assumed until concrete files and event coverage are identified.

For Level 3, the relevant question would be whether posterior samples can be matched by source/pipeline well enough to compare IMR and pSEOBNR posterior-propagated `f_Kerr` distributions for common events.

### pyRing / ringdown-specific products

pyRing or other ringdown-specific products are plausible sources for posterior samples of observed ringdown quantities, including frequency and damping-time parameters. These products are conceptually distinct from IMR remnant mass/spin posterior samples.

They could help audit whether published `freq_hz` and `tau_ms` summaries are representative of posterior distributions, and whether observed-side frequency posteriors contribute to the sign pattern. They do not by themselves solve remnant median mapping unless they also include, or can be paired with, joint remnant `M_final`/`chi_final` posterior samples under a compatible provenance model.

### Capano / Isi / Giesler / other single-event products

Single-event or small-cohort analyses may provide useful posterior products for specific events, especially benchmark events or ringdown-focused studies. These can be valuable for case studies or sanity checks.

They do not close the population-level Paper 4 question unless the event coverage, parameter definitions, and source conventions are consistent enough to support the sign-asymmetry cohort. Heterogeneous sources and low `N` would keep the result methodological rather than population-resolved.

O4 or later special events are outside the main Paper 4 scope unless a separate future plan explicitly extends the dataset and provenance policy.

## Inventory table

| source_family | expected_samples | needed_for_level2 | current_status | blocker | action_if_pursued |
|---|---|---|---|---|---|
| GWOSC / LVK PE releases | Event-level posterior samples for remnant mass/spin may exist, depending on event and PE run. | Joint `M_final` and `chi_final` samples; frame convention; event/run provenance. | `likely_available` | No concrete local file inventory has been verified for the Paper 4 event set. | Search release inventories for the exact Paper 4 events and PE runs; record file paths, parameter names, and conventions before any computation. |
| GWTC-2 TGR / O3a TGR products | Possible TGR/ringdown products, potentially including agnostic or pyRing-style posteriors. | Joint remnant posterior samples matching the tabulated IMR provenance; observed ringdown posteriors if available. | `unknown` | Local inputs are scalar tabular summaries; no posterior products are verified locally. | Identify whether official TGR products include posterior samples for the phase1 events and whether they match the source table provenance. |
| GWTC-4 pSEOBNR source | Possible posterior products in a separate release, not in the local CSV. | Joint remnant posterior samples for the pSEOBNR source or compatible PE run; event coverage for the 9-row cohort. | `unknown` | Current local data are scalar summaries; no release files are verified. | Locate the corresponding release, if any, and map event IDs, PE runs, and field names before Level 2/3 planning. |
| pyRing / ringdown-specific products | Frequency and damping posterior samples may exist for selected events. | Observed-side `f_220`/`tau` posteriors; optionally compatible remnant samples if packaged or linkable. | `partial` | Ringdown posteriors are not equivalent to joint remnant mass/spin posteriors; coverage may be event-limited. | Use only after separating observed-side posterior auditing from remnant posterior propagation. |
| Capano / Isi / Giesler / other single-event products | Event-specific posterior samples or reconstructed ringdown quantities may exist. | Useful for case studies; not sufficient for population Level 2 unless coverage and conventions align. | `partial` | Low `N`, heterogeneous methods, and source-convention mismatch risk. | Treat as targeted validation examples, not as the main population closure. |
| Published scalar summaries only | Medians and uncertainties for remnant and QNM quantities. | Insufficient for full Level 2; can only support weak approximations. | `available` | No joint posterior shape or covariance. | Use only for a clearly labeled Level 1b approximation if posterior samples cannot be located. |

## Verdict

Level 2 must not be declared available until concrete posterior files are verified for the relevant events, parameter names, source/detector-frame conventions, and source-pipeline provenance.

If only published scalar summaries are available, the strongest possible next step is Level 1b: an exploratory and weak approximation to central-value bias. Such a calculation would not resolve the median-mapping criticism.

Without joint posterior samples for `M_final` and `chi_final`, Paper 4 cannot fully evaluate `median(f_Kerr(M_final, chi_final))` against `f_Kerr(median(M_final), median(chi_final))`.

## Immediate next step

Create a non-computational release-inventory checklist for the Paper 4 event set, listing event IDs, desired PE run/source, candidate release family, required parameter names, frame convention, and local/remote file status. No downloads or posterior propagation should occur until that checklist is complete.
