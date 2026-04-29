# Paper 4 — Deposit Decision

## Scope

This document records the current methodological decision for Fase 4 / Paper 4. It does not execute a deposit, modify the README, regenerate tables, rerun analyses, or change any source data.

## Current Phase 4 state

The main result is a reproducible methodological audit, not a candidate search result. Paper 4 finds no robust individual frequency-only outliers at `|residual_f| >= 2`, and it does not identify candidate-level Kerr deviations.

The frequency channel shows a positive population-level sign asymmetry in published 220 ringdown observables across two source/pipeline choices: GWTC-2 TGR IMR and GWTC-4 pSEOBNR. Common events preserve the positive sign across the two sources.

The permitted interpretation is:

```text
methodological_systematics_limited
```

Explicit limits:

- No beyond-Kerr claim.
- No candidate catalogue.
- No population-level Kerr-violation claim.
- No gamma/damping physical claim.
- No claim that remnant median mapping is resolved without posterior samples.
- No claim that residuals are independent draws without source/provenance caveats.

## Deposit criteria

| criterion | status | note |
|---|---|---|
| Clear methodological result | `pass` | The result is framed as a reproducible sign-asymmetry audit with no candidate claim. |
| Permanent scripts | `pass` | `tools/paper4_build_summary_tables.py` regenerates the final summary tables from existing scalar-summary inputs. |
| Reproducible outputs | `partial` | Summary tables have been generated, but should be regenerated after the final commit state is clean. |
| Language avoids candidate/new-physics claims | `pass` | Current docs explicitly forbid beyond-Kerr, candidate-catalogue, and Kerr-violation interpretations. |
| Limitations explicit | `pass` | Gamma limitations, remnant mapping limits, posterior-sample availability, and modeling-systematics context are documented. |
| README updated | `fail` | README has intentionally not been updated yet. This should happen only at the end if publication/deposit is chosen. |
| Final table versionable or regenerable | `pass` | Tables are regenerable through `python3 tools/paper4_build_summary_tables.py`; whether to version `runs/paper4_summary_tables/` remains a release-policy decision. |
| Source provenance | `partial` | Source families and CSV provenance are documented; final release should still verify that no ambiguous untracked interpretive files remain. |
| Level 2 posterior samples status | `partial` | Availability inventory exists, but concrete posterior files are not verified. Level 2 remains pending. |

## Recommended decision

Do not deposit yet.

The block is close to a technical-audit/reproducibility note, but deposit should wait until:

- the final docs and summary-table script are reviewed and committed intentionally;
- the untracked Spanish bibliographic document is either incorporated, ignored by release policy, or removed from the release scope;
- summary tables are regenerated from the committed script in a clean or intentionally understood working-tree state;
- the README is updated at the end only if publication/deposit is chosen;
- Level 2 posterior-sample status is described honestly as pending, not solved.

## Condition under which deposit is appropriate

Deposit may be appropriate as a technical audit / reproducibility note if all of the following remain true:

- The interpretation stays systematic-limited and methodological.
- The summary outputs regenerate from the permanent script.
- No Kerr-violation, beyond-Kerr, or candidate-catalogue claim is made.
- Gamma/damping remains documented as systematics-limited and excluded from physical claims.
- Level 2 remnant posterior propagation is declared as a limitation, not as completed.
- The repository state is curated so that release artifacts and non-release notes are unambiguous.

## Condition under which deposit is not appropriate

Do not deposit if any of the following become true:

- The narrative depends on outputs that cannot be regenerated.
- The work is presented as a candidate search or candidate catalogue.
- Gamma/damping residuals are reopened as physical claims.
- Source provenance is left ambiguous.
- Remnant median mapping is described as solved without posterior samples.
- The writeup implies new physics, evidence for Kerr violation, or a population-level Kerr-violation claim.

## Recommended next action

Review the full diff first, then prepare a focused commit containing the final methodological documents, the summary-table script, and any intentionally retained release artifacts.

If the diff is clean and the Spanish untracked document is resolved, the next operational step can be a final regeneration of the summary tables followed by README update only if Fase 4 is explicitly moving toward a technical-audit deposit.
