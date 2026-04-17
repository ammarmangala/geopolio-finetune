---
name: documentation-enforcer
description: "Use when updating docs, adding new workflows, or checking whether repository docs still match the codebase."
argument-hint: "Docs page, workflow, or area to document"
---

# Documentation Enforcer

Use this skill when documentation needs to stay aligned with the repository.

## When to Use

- A new workflow, file, or folder is added.
- Existing docs drift away from the scripts or notebook.
- A reader needs a single place to understand the repo.
- You want to check whether the docs index still covers the project.

## What to Check

- `docs/README.md` stays current as the docs entry point.
- `docs/guides/README.md` stays current as the workflow guide index.
- `docs/guides/ARCHITECTURE.md` matches the actual repo layout.
- `docs/guides/DATASET_WORKFLOW.md` matches the current dataset rules.
- `docs/guides/FINETUNING_NOTES.md` matches the notebook behavior.
- `docs/guardrails/README.md` stays current for customization assets.
- New workflow files are documented before the repo grows further.

## Procedure

1. Identify the area that changed.
2. Check whether the docs index mentions it.
3. Check whether the relevant guide still matches the code.
4. Update the docs before the change spreads to more files.
5. Keep the writing short, direct, and beginner-friendly.

## Output Format

Return:
- docs that need updates
- why they are stale or missing
- the minimum doc changes needed
- whether the docs set is coherent after the update
---
name: documentation-enforcer
description: "Use when updating docs, adding new workflows, or checking whether repository docs still match the codebase."
argument-hint: "Docs page, workflow, or area to document"
---

# Documentation Enforcer

Use this skill when documentation needs to stay aligned with the repository.

## When to Use

- A new workflow, file, or folder is added.
- Existing docs drift away from the scripts or notebook.
- A reader needs a single place to understand the repo.
- You want to check whether the docs index still covers the project.

## What to Check

- `docs/README.md` stays current as the docs entry point.
- `docs/ARCHITECTURE.md` matches the actual repo layout.
- `docs/DATASET_WORKFLOW.md` matches the current dataset rules.
- `docs/FINETUNING_NOTES.md` matches the notebook behavior.
- New workflow files are documented before the repo grows further.

## Procedure

1. Identify the area that changed.
2. Check whether the docs index mentions it.
3. Check whether the relevant guide still matches the code.
4. Update the docs before the change spreads to more files.
5. Keep the writing short, direct, and beginner-friendly.

## Output Format

Return:
- docs that need updates
- why they are stale or missing
- the minimum doc changes needed
- whether the docs set is coherent after the update
