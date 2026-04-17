# Customization and Guardrails

This page is the catalog for every repository customization that keeps the project tidy as it grows.

## Why this page exists

The repository already has a few different customization types:
- skills for repeatable workflows
- an agent for structural review
- a hook for session-start reminders

This page explains what each one is for, when to use it, why it exists, and the best practices to follow.

## The rule for naming

Use a generic name when the customization can be reused in other workspaces.
Use a `geopolio-` prefix only when the customization is specific to this repository.

That keeps the repo tidy and makes the reusable parts easier to copy elsewhere.

## Quick inventory

| Name | Type | Scope | Purpose | When to use | Why it exists |
|---|---|---|---|---|---|
| `documentation-enforcer` | Skill | Generic | Keep docs aligned with the codebase | When docs may be stale, incomplete, or missing | Prevent documentation drift |
| `geopolio-dataset-workflow` | Skill | Geopolio-specific | Manage dataset expansion, balancing, and validation | When preparing training data | Protect the dataset quality rules for this project |
| `geopolio-dataset-merge-validate` | Skill | Geopolio-specific | Merge and normalize datasets before expansion or training | When combining seed datasets or cleaning intermediate files | Prevent bad schema and duplicate inputs from entering the pipeline |
| `geopolio-finetune-run` | Skill | Geopolio-specific | Run and recover the notebook training workflow | When training, resuming, or adjusting finetuning runs | Keep checkpointing, best-model selection, and final saves consistent |
| `geopolio-evaluation-workflow` | Skill | Geopolio-specific | Compare model outputs and benchmark candidates | When deciding whether one model is better than another | Make model comparison repeatable and practical |
| `architecture-auditor` | Agent | Generic | Review structure, dependency flow, and separation of concerns | When assessing architecture risk or growth issues | Give a read-only structural review without editing files |
| `docs-reminder` | Hook | Generic | Remind the user to check docs before workflow changes | At session start | Keep the docs visible while working |

## How the pieces fit together

### Skills
Skills are best for repeatable workflows.
They load on demand and should contain the instructions needed to complete one family of tasks.

Use a skill when:
- the task repeats often
- the workflow has a clear procedure
- the workflow benefits from a shared checklist

Best practices for skills:
- keep the description specific and keyword-rich
- keep the steps short and deterministic
- load references only when the skill needs them
- use a generic name unless the task is repo-specific

### Agents
Agents are best for a focused persona with a narrow job.
They are useful when you want a review or analysis without editing files.

Use an agent when:
- you want a specialized read-only review
- you want a structured verdict with clear output
- you do not need a full multi-step workflow skill

Best practices for agents:
- keep the role narrow
- use only the tools the role needs
- state what the agent must not do
- keep the output format explicit

### Hooks
Hooks are best for deterministic enforcement.
They run automatically at session or tool boundaries.

Use a hook when:
- you want a reminder or validation to happen every session
- you want behavior to be enforced, not just suggested
- you want to inject standard context before work starts

Best practices for hooks:
- keep the hook small and auditable
- avoid long-running logic
- do not put secrets in hook scripts
- use hooks for enforcement, not for broad guidance

## Detailed asset guide

### `documentation-enforcer`

**Type:** Skill

**Purpose:**
Keep documentation aligned with the repository structure and behavior.

**When it is used:**
- when a workflow changes
- when docs may be stale
- when a new file or process needs a doc page

**Why it is used:**
Documentation is the easiest thing to let drift as a project grows.
This skill keeps the docs index, architecture guide, and workflow notes in sync.

**Best practices:**
- update docs before or alongside code changes
- check the docs index first
- keep the language short and direct
- make sure the docs set stays coherent as a whole

**What it should return:**
- which docs need updates
- why they are stale or missing
- the smallest necessary doc changes
- whether the docs set is coherent after the update

### `geopolio-dataset-workflow`

**Type:** Skill

**Purpose:**
Expand, rebalance, validate, and select Geopolio training datasets.

**When it is used:**
- expanding to a larger target size
- rebalancing a dataset before training
- checking whether a dataset is safe to train on
- deciding which dataset file the notebook should load

**Why it is used:**
The repo has strict dataset rules: uniqueness, canonical labels, and balance across categories, regions, and risk scores.

**Best practices:**
- always prefer the balanced dataset for training
- do not train on duplicated inputs
- keep intermediate outputs separate from the final training file
- validate size, uniqueness, and balance before training

### `geopolio-dataset-merge-validate`

**Type:** Skill

**Purpose:**
Merge datasets, remove duplicates, and normalize output schema before expansion or training.

**When it is used:**
- combining seed datasets
- cleaning an intermediate file
- normalizing category labels
- verifying schema consistency

**Why it is used:**
Bad schema or duplicate content should be removed before a dataset enters the expansion or training pipeline.

**Best practices:**
- drop invalid rows rather than preserving them
- map aliases to canonical labels
- deduplicate before balancing
- verify that `instruction`, `input`, and JSON `output` are all present

### `geopolio-finetune-run`

**Type:** Skill

**Purpose:**
Run and maintain the notebook-based finetuning workflow.

**When it is used:**
- running the notebook end to end
- changing the training dataset
- adjusting hyperparameters
- resuming after a runtime reset
- choosing the best checkpoint or final model

**Why it is used:**
The notebook is the place where training happens, but the training run must stay reproducible, checkpointed, and recoverable.

**Best practices:**
- use the balanced dataset by default
- keep checkpoint saving enabled
- keep the best checkpoint, not just the last one
- save both the final model and tokenizer
- compare `train_loss` and `eval_loss` before calling a run complete

### `geopolio-evaluation-workflow`

**Type:** Skill

**Purpose:**
Compare Geopolio models and review generated outputs.

**When it is used:**
- comparing a finetuned model with a base model
- reviewing benchmark outputs
- checking whether a checkpoint is actually better
- building a repeatable evaluation checklist

**Why it is used:**
A model that looks good numerically may still be worse in practice if it gets categories, regions, or confidence wrong.

**Best practices:**
- compare the same prompt set across candidates
- evaluate consistency, not just verbosity
- watch for category drift, region drift, and overconfident scores
- record the dataset, model names, prompt set, and failure modes

### `architecture-auditor`

**Type:** Agent

**Purpose:**
Review repository structure, dependency flow, and separation of concerns.

**When it is used:**
- when you want a read-only architecture review
- when you want to know whether a change hurts growth or maintainability
- when deciding whether to move logic out of notebooks or scripts

**Why it is used:**
Architecture tends to drift slowly, then suddenly becomes hard to maintain. This agent gives a deliberate structural review before that happens.

**Best practices:**
- keep the notebook thin
- keep reusable logic in `src`
- keep orchestration in scripts
- update docs alongside structural changes

### `docs-reminder`

**Type:** Hook

**Purpose:**
Remind you at session start to check the docs before changing workflow code.

**When it is used:**
- automatically at session start
- before new work begins

**Why it is used:**
The docs are easiest to forget when the project is moving quickly. The hook keeps them visible.

**Best practices:**
- keep the hook small and auditable
- use it as a reminder, not as a replacement for docs
- keep the message focused on the main docs pages

## Which asset to use when

- Use `documentation-enforcer` when docs may be stale.
- Use `geopolio-dataset-workflow` when the training dataset is changing.
- Use `geopolio-dataset-merge-validate` when combining or cleaning datasets.
- Use `geopolio-finetune-run` when training or recovering the notebook.
- Use `geopolio-evaluation-workflow` when comparing models or checkpoints.
- Use `architecture-auditor` when reviewing structure and growth risks.
- Let `docs-reminder` run automatically at session start.

## Short version

If the task is reusable across workspaces, give it a generic name.
If it is specific to this repository, prefix it with `geopolio-`.
