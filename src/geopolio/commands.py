"""CLI entrypoints for Geopolio dataset workflows."""

from __future__ import annotations

import argparse
import json
import os
import random
import time
from pathlib import Path

from openai import OpenAI

from .dataset import (
    CATEGORIES,
    DECADES,
    EXAMPLE,
    GENERATION_DECADES,
    REGIONS,
    build_balanced_dataset,
    build_sample,
    deduplicate,
    deduplicate_exact,
    load_json,
    normalize_sample,
    report,
    save_json,
    summarize_distribution,
    validate_sample,
    pick_underrepresented,
)


def _build_prompt(batch_size: int, categories: list[str], regions: list[str], decade_info: tuple[str, list[str]], existing_inputs: list[str]) -> str:
    decade_label, decade_examples = decade_info
    existing_sample = random.sample(existing_inputs, min(5, len(existing_inputs))) if existing_inputs else []

    avoid_section = ""
    if existing_sample:
        avoid_section = f"""
AVOID DUPLICATES - Do NOT generate scenarios similar to these already existing ones:
{chr(10).join(f'- {s}' for s in existing_sample)}
"""

    return f"""You are a data generation system for training an AI geopolitical risk model.

TASK: Generate exactly {batch_size} unique training samples.

STRICT OUTPUT RULES:
- Return ONLY a valid JSON array. No preamble, no explanation, no markdown, no code blocks.
- Every output field must be a properly escaped JSON string.
- Complete all {batch_size} items. Do not truncate.

EACH ITEM MUST FOLLOW THIS EXACT STRUCTURE:
{{"instruction": "Analyze the geopolitical risk of the following situation for European retail investors.", "input": "<scenario>", "output": "{{\\\"risk_score\\\": <1-10>, \\\"region\\\": \\\"<region>\\\", \\\"category\\\": \\\"<category>\\\", \\\"impact\\\": \\\"<Low|Moderate|High|Critical>\\\", \\\"analysis\\\": \\\"<analysis>\\\"}}"}}

DECADE FOCUS FOR THIS BATCH: {decade_label}
Draw inspiration from events like:
{chr(10).join(f'- {e}' for e in decade_examples)}

CATEGORY DISTRIBUTION FOR THIS BATCH (spread evenly):
{', '.join(categories)}

REGION DISTRIBUTION FOR THIS BATCH (vary widely):
{', '.join(regions)}

RISK SCORE DISTRIBUTION:
- Scores 2-4: 20% of samples
- Scores 5-7: 50% of samples
- Scores 8-10: 30% of samples

{avoid_section}

QUALITY RULES:
- Every scenario must be realistic and historically plausible for {decade_label}
- Analysis must reference specific European indices, ETFs, companies, or sectors by name
- No two scenarios can be identical or near-identical
- Vary severity, geography, and investor impact per item
- Keep analysis concise but expert-level, 3-5 sentences

STYLE REFERENCE - Match this example exactly:
{json.dumps(EXAMPLE, ensure_ascii=False)}

Generate all {batch_size} items now."""


def _save_checkpoint(path: Path, samples: list[dict]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        json.dump(samples, handle, ensure_ascii=False)


def _load_checkpoint(path: Path) -> list[dict]:
    if path.exists():
        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
        print(f"Checkpoint gevonden: {len(data)} samples hersteld.")
        return data
    return []


def _generate_batch(client: OpenAI, model: str, batch_size: int, decade_info: tuple[str, list[str]], existing_inputs: list[str]) -> list[dict]:
    categories_sample = random.sample(CATEGORIES, min(6, len(CATEGORIES)))
    regions_sample = random.sample(REGIONS, min(8, len(REGIONS)))
    prompt = _build_prompt(batch_size, categories_sample, regions_sample, decade_info, existing_inputs)

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.9,
        max_tokens=16000,
    )

    content = response.choices[0].message.content.strip()
    if content.startswith("```"):
        content = content.split("```")[1]
        if content.startswith("json"):
            content = content[4:]
    content = content.strip()

    return json.loads(content)


def generate_dataset_main() -> None:
    api_key = os.environ.get("OPENAI_API_KEY", "sk-jouw-key-hier")
    target = 5000
    batch_size = 50
    output_file = "geopolio_dataset_5000s_multidecade.json"
    checkpoint_file = Path("checkpoint.json")
    model = "gpt-5.4-mini"

    client = OpenAI(api_key=api_key)

    print("Geopolio Dataset Generator gestart")
    print(f"Target: {target} samples | Batch size: {batch_size} | Model: {model}")
    print("─" * 60)

    all_samples = _load_checkpoint(checkpoint_file)
    existing_inputs = [sample["input"] for sample in all_samples]

    decade_weights = [0.2, 0.3, 0.5]
    batch_num = 0
    errors = 0
    max_errors = 10

    while len(all_samples) < target:
        remaining = target - len(all_samples)
        current_batch_size = min(batch_size, remaining)
        batch_num += 1
        decade_info = random.choices(GENERATION_DECADES, weights=decade_weights, k=1)[0]

        print(f"Batch {batch_num} | Decade: {decade_info[0]} | Generating {current_batch_size} samples...", end=" ")

        try:
            raw_samples = _generate_batch(client, model, current_batch_size, decade_info, existing_inputs[-50:])
            valid = [sample for sample in raw_samples if validate_sample(sample)]
            invalid_count = len(raw_samples) - len(valid)

            all_samples.extend(valid)
            all_samples = deduplicate(all_samples)
            existing_inputs = [sample["input"] for sample in all_samples]

            print(f"Got {len(raw_samples)} | Valid: {len(valid)} | Invalid: {invalid_count} | Total: {len(all_samples)}/{target}")
            _save_checkpoint(checkpoint_file, all_samples)
            errors = 0

        except Exception as exc:
            errors += 1
            print(f"ERROR ({errors}/{max_errors}): {exc}")
            if errors >= max_errors:
                print("Te veel fouten. Gestopt.")
                break
            time.sleep(10)
            continue

        time.sleep(2)

    final = all_samples[:target]
    with open(output_file, "w", encoding="utf-8") as handle:
        json.dump(final, handle, indent=2, ensure_ascii=False)

    print("─" * 60)
    print(f"Klaar! {len(final)} samples opgeslagen in {output_file}")

    from collections import Counter

    categories = [json.loads(sample["output"])["category"] for sample in final]
    print("\nCategory verdeling:")
    for category, count in sorted(Counter(categories).items(), key=lambda item: -item[1]):
        print(f"  {category}: {count}")


def _parse_expand_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Expand an existing Geopolio dataset locally.")
    parser.add_argument("--source", default="data/geopolio_dataset_2099s_global_multidecade.json")
    parser.add_argument("--output", default="data/geopolio_dataset_5000s_global_multidecade.json")
    parser.add_argument("--checkpoint", default="data/geopolio_dataset_5000s_global_multidecade.checkpoint.json")
    parser.add_argument("--target-size", type=int, default=5000)
    parser.add_argument("--batch-size", type=int, default=100)
    parser.add_argument("--seed", type=int, default=42)
    return parser.parse_args()


def _load_seed_samples(source: Path, checkpoint: Path) -> list[dict]:
    source_samples = deduplicate(load_json(source))
    if checkpoint.exists():
        resumed = deduplicate(load_json(checkpoint))
        if len(resumed) >= len(source_samples):
            return resumed
    return source_samples


def _extend_samples(samples: list[dict], target_size: int, batch_size: int, checkpoint: Path) -> list[dict]:
    while len(samples) < target_size:
        category_counts, region_counts = summarize_distribution(samples)
        generated: list[dict] = []
        attempts = 0

        while len(generated) < min(batch_size, target_size - len(samples)) and attempts < batch_size * 20:
            attempts += 1
            category = pick_underrepresented(category_counts, CATEGORIES)
            region = pick_underrepresented(region_counts, list(REGIONS))
            sample = build_sample(region=region, category=category)
            merged = deduplicate([*samples, *generated, sample])
            if len(merged) == len(samples) + len(generated) + 1 and validate_sample(sample):
                generated.append(sample)
                category_counts[category] += 1
                region_counts[region] += 1

        if not generated:
            raise RuntimeError("Could not generate additional unique samples.")

        samples = deduplicate([*samples, *generated])
        save_json(checkpoint, samples)
        print(f"Added {len(generated)} samples | total {len(samples)}/{target_size}")

    return samples[:target_size]


def expand_dataset_main() -> None:
    args = _parse_expand_args()
    random.seed(args.seed)

    source = Path(args.source)
    output = Path(args.output)
    checkpoint = Path(args.checkpoint)

    if not source.exists():
        raise FileNotFoundError(f"Source dataset not found: {source}")

    samples = _load_seed_samples(source, checkpoint)
    samples = deduplicate([sample for sample in samples if validate_sample(sample)])

    print(f"Loaded {len(samples)} samples from {source}")

    if len(samples) >= args.target_size:
        final_samples = samples[: args.target_size]
        save_json(output, final_samples)
        print(f"Source already meets target. Wrote {len(final_samples)} samples to {output}")
        return

    final_samples = _extend_samples(samples=samples, target_size=args.target_size, batch_size=args.batch_size, checkpoint=checkpoint)
    save_json(output, final_samples)
    print(f"Completed. Wrote {len(final_samples)} samples to {output}")


def _parse_rebalance_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a fully balanced Geopolio dataset.")
    parser.add_argument(
        "--source",
        default="data/geopolio_dataset_5000s_global_multidecade.json",
        help="Source dataset used for normalization and sample reuse.",
    )
    parser.add_argument(
        "--output",
        default="data/geopolio_dataset_5000s_global_multidecade_balanced.json",
        help="Balanced output dataset.",
    )
    parser.add_argument("--target-size", type=int, default=5000, help="Final dataset size.")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for deterministic balancing.")
    return parser.parse_args()


def rebalance_dataset_main() -> None:
    args = _parse_rebalance_args()
    random.seed(args.seed)

    source = Path(args.source)
    output = Path(args.output)

    raw_samples = load_json(source)
    normalized = []
    for sample in deduplicate_exact(raw_samples):
        fixed = normalize_sample(sample)
        if fixed is not None:
            normalized.append(fixed)

    balanced = build_balanced_dataset(normalized, args.target_size)
    save_json(output, balanced)
    print(f"Wrote {len(balanced)} balanced samples to {output}")
    print(json.dumps(report(balanced), indent=2))


__all__ = [
    "expand_dataset_main",
    "generate_dataset_main",
    "rebalance_dataset_main",
]
