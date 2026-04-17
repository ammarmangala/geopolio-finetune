from __future__ import annotations

import json
import sys


MESSAGE = (
    "Check docs/README.md, docs/ARCHITECTURE.md, docs/DATASET_WORKFLOW.md, and "
    "docs/FINETUNING_NOTES.md before changing workflow code."
)


def main() -> None:
    _ = sys.stdin.read()
    json.dump({"continue": True, "systemMessage": MESSAGE}, sys.stdout)


if __name__ == "__main__":
    main()
