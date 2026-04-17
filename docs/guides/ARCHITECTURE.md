# Architecture Overview

This repository is small, but it already has a shape that can scale if the responsibilities stay separated.

## Current architecture

- `data/` holds source datasets, generated datasets, and checkpoints.
- `docs/` explains how to use the project safely.
- `notebooks/` contains the interactive finetuning workflow.
- `scripts/generation/` contains dataset generation, expansion, and rebalancing entrypoints.
- `src/geopolio/` now contains shared dataset logic and CLI entrypoints.
- `tests/` contains checks for dataset helper behavior.
- `models/` is the place for saved model artifacts.

## Main flow

1. Generate or expand a dataset.
2. Rebalance and validate it.
3. Train the notebook against the balanced file.
4. Save the best checkpoint and final model.
5. Evaluate candidate outputs before changing the workflow again.

## Design rule

Keep reusable logic in `src/geopolio`.
Keep orchestration in `scripts/generation`.
Keep experimentation in `notebooks`.
Keep explanations in `docs`.

That split matters because it prevents the notebook from becoming the only place where the project can be understood.

## What is sustainable

The project is sustainable if these responsibilities stay separated:
- dataset constants and validation rules live in one shared module
- CLI scripts are thin wrappers
- notebooks stay focused on runs, not core logic
- tests protect balance and schema rules
- docs explain the workflow in plain language

## What will break first

If the repo grows without refactoring, these are the first pressure points:
- duplicated constants in multiple scripts
- notebook cells that drift from the scripts
- unclear dataset lineage between intermediate and final files
- manual validation by memory instead of tests

## Recommended next step

As the project grows, keep moving shared logic out of notebook cells and scripts into `src/geopolio`.

## Related docs

- [Guides index](./README.md)
- [Root docs index](../README.md)
- [Dataset workflow](./DATASET_WORKFLOW.md)
- [Finetuning notes](./FINETUNING_NOTES.md)
- [Customization and guardrails](../guardrails/CUSTOMIZATION.md)
