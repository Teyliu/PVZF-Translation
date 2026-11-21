
import json
import os
from pathlib import Path

# Set working directory to the script's own directory
script_dir = Path(__file__).resolve().parent
parent_dir = script_dir.parent
os.chdir(script_dir)

# File locations
strings_path = (
    parent_dir / "PvZ_Fusion_Translator"
    / "Localization" / "English" / "Strings"
    / "translation_strings.json"
)

almanac_path = (
    parent_dir / "PvZ_Fusion_Translator"
    / "Localization" / "English" / "Almanac"
    / "ShootingAlmanacTranslate.json"
)

# Load files
with open(strings_path, "r", encoding="utf-8") as f:
    translations = json.load(f)

with open(almanac_path, "r", encoding="utf-8") as f:
    almanac = json.load(f)

# Read original text for line-number lookup
with open(almanac_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

matched = 0
unmatched = 0
unmatched_descriptions = []

# Iterate through all plants and buffs
for plant in almanac["plants"]:
    for buff in plant.get("buffs", []):
        description = buff.get("descriptionOverride", "")

        if not description.strip():
            continue

        if description in translations:
            buff["descriptionOverride"] = translations[description]
            matched += 1
        else:
            unmatched += 1

            # Find the original line containing this description
            for line_number, line in enumerate(lines, start=1):
                if '"descriptionOverride"' in line:
                    if description in line:
                        unmatched_descriptions.append(
                            (line_number, plant["plant"], description)
                        )
                        break

# Save modified JSON
with open(almanac_path, "w", encoding="utf-8") as f:
    json.dump(almanac, f, ensure_ascii=False, indent=4)

# Print results
print(f"Replaced: {matched}")
print(f"Unmatched non-empty descriptions: {unmatched}")
print("\nUnmatched descriptions:")

for line_number, plant, description in unmatched_descriptions:
    print(f"Line {line_number} [{plant}]: {description!r}")

print(f"\nWorking directory: {Path.cwd()}")
