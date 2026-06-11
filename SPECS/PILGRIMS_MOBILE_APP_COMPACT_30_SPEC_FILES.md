# ARCHIVED — Pilgrims Mobile App compact 30-file spec draft

## Document status
- **Type:** Historical planning artifact
- **Priority:** Non-normative
- **Audience:** Maintainers, reviewers, AI agents
- **Status:** Superseded by the current 31-spec system and machine-readable contracts

This file is intentionally retained only as historical context for the earlier compact documentation architecture.

It is **not** part of the normative specification system for implementation, review, release, or AI-agent work.

Current source of truth:
- `README.md`
- `SPECS/01_README_AND_MASTER_INDEX.md`
- `SPECS/31_QUALITY_FIRST_HARDENING_AMENDMENTS.md`
- `SPECS/CONTRACTS/README.md`
- `SPECS/CONTRACTS/*`
- `tools/specs/validate_spec_contracts.py`

Normative rule:
- Treat the live repo as a 31 normative Markdown spec system plus machine-readable contract artifacts.
- Do not use this archived 30-file draft to infer current filenames, file counts, authority hierarchy, dependencies, scope, release gates, or implementation tasks.
- If this file conflicts with any current spec or contract artifact, the current spec/contract wins.

## Why this archive marker exists

The project previously used a compact 30-file planning model. The system has since evolved to include:
- `SPECS/31_QUALITY_FIRST_HARDENING_AMENDMENTS.md`
- contract artifacts under `SPECS/CONTRACTS/`
- baseline contract validation under `tools/specs/validate_spec_contracts.py`

Keeping this file without an archive marker created a risk that human contributors or AI agents would follow obsolete governance language.

End of archived marker.
