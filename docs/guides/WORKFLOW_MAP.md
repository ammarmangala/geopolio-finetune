# Workflow Map

Use this page if you want a fast overview of how the repository fits together.

## Dataset workflow

1. Start with the source or seed dataset.
2. Expand it to a larger target size if needed.
3. Rebalance the expanded dataset.
4. Validate uniqueness and class balance.
5. Train only on the balanced file.

See [DATASET_WORKFLOW.md](./DATASET_WORKFLOW.md).

## Finetuning workflow

1. Load the balanced dataset.
2. Split into train and eval sets.
3. Train with checkpoints enabled.
4. Keep the checkpoint with the best eval loss.
5. Save the final model and tokenizer.

See [FINETUNING_NOTES.md](./FINETUNING_NOTES.md).

## Architecture workflow

1. Keep reusable logic in `src/geopolio`.
2. Keep command-line orchestration in `scripts/generation`.
3. Keep notebooks for experimentation.
4. Add tests whenever a shared rule changes.

See [ARCHITECTURE.md](./ARCHITECTURE.md).
