import json

files = [
    "data/geopolio_dataset_200s_global.json",
    "data/geopolio_dataset_2000s_global.json",
]

combined = []
for f in files:
    with open(f) as file:
        data = json.load(file)
        combined.extend(data)
        print(f"{f}: {len(data)} samples")

# Deduplicatie
seen = set()
unique = []
for s in combined:
    key = s["input"].strip().lower()[:100]
    if key not in seen:
        seen.add(key)
        unique.append(s)

print(f"\nTotaal voor dedup: {len(combined)}")
print(f"Totaal na dedup: {len(unique)}")

with open("data/geopolio_dataset_2200s_multidecade.json", "w") as f:
    json.dump(unique, f, indent=2, ensure_ascii=False)

print("Opgeslagen: geopolio_dataset_2200s_multidecade.json")