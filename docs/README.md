# Geopolio Docs Index

Start here if you are new to the repository.

## What this repo does

This project builds and finetunes a geopolitical risk model for European retail investors.
It has three main layers:
- dataset generation and balancing
- notebook-based finetuning
- model evaluation and iteration

## Read this first

1. [Guides overview](./guides/README.md)
2. [Architecture overview](./guides/ARCHITECTURE.md)
3. [Dataset workflow](./guides/DATASET_WORKFLOW.md)
4. [Workflow map](./guides/WORKFLOW_MAP.md)
5. [Finetuning notes](./guides/FINETUNING_NOTES.md)
6. [Customization and guardrails](./guardrails/README.md)

## File guide

### [guides/README.md](./guides/README.md)
Overview of the main workflow documents.

### [guardrails/README.md](./guardrails/README.md)
Overview of the skills, agent, and hook that keep the repo tidy.

## Current recommended defaults

- Training dataset: `data/geopolio_dataset_5000s_global_multidecade_balanced.json`
- Intermediate expanded dataset: `data/geopolio_dataset_5000s_global_multidecade.json`
- Intermediate checkpoint: `data/geopolio_dataset_5000s_global_multidecade.checkpoint.json`
- Notebook: `notebooks/geopolio_finetune.ipynb`

## If you are stuck

- If you are unsure which dataset to use, read [guides/DATASET_WORKFLOW.md](./guides/DATASET_WORKFLOW.md).
- If training behaves oddly, read [guides/FINETUNING_NOTES.md](./guides/FINETUNING_NOTES.md).
- If you want to change the project structure, read [guides/ARCHITECTURE.md](./guides/ARCHITECTURE.md).
- If you want the short version of the full flow, read [guides/WORKFLOW_MAP.md](./guides/WORKFLOW_MAP.md).
- If you want the guardrails and customization setup, read [guardrails/CUSTOMIZATION.md](./guardrails/CUSTOMIZATION.md).

## Short version

Use the balanced dataset, keep the notebook thin, and move reusable logic into `src/geopolio`.
