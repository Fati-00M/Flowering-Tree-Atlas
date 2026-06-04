import csv
import os

base_dir = r"d:\Climate Change data\FLOWERING TREES PROJECT"
input_path = os.path.join(base_dir, "flowering_trees_combined.csv")
output_path = os.path.join(base_dir, "flowering_trees_simplified.csv")

selected_cols = [
    'scientificname',
    'dominant biome',
    'dominant climatic moisture index',
    'flower color', 'flower sex', 'flowering lag time: number of days from exposition start to flowering',
    'flowering requirement (requirement for fertility)', 'fruit type', 'plant flowering', 'plant growth form',
    'plant growth temperature range', 'plant height', 'plant human usage types', 'plant lifespan (longevity)',
    'plant lifespan: age trees reach in forested stands', 'plant woodiness', 'seed germination base temperature',
    'seed germination base water potential', 'seed germination lag time', 'seed germination requirement',
    'seed germination temperature', 'seed germination type', 'wood growth ring distinction',
    'Category of Use', 'Crop Wild Relative',
    'native to', 'native range'
]

print("Reading combined CSV and generating simplified version...")
if not os.path.exists(input_path):
    print(f"Error: Combined CSV not found at {input_path}")
    exit(1)

with open(input_path, "r", encoding="utf-8", errors="replace") as f_in:
    reader = csv.DictReader(f_in)
    
    # Check that all selected columns actually exist in the source
    existing_cols = reader.fieldnames
    missing_cols = [col for col in selected_cols if col not in existing_cols]
    if missing_cols:
        print(f"Warning: The following selected columns are missing from the input CSV: {missing_cols}")
        # Filter to only keep columns that actually exist
        selected_cols = [col for col in selected_cols if col in existing_cols]

    with open(output_path, "w", encoding="utf-8", newline="") as f_out:
        writer = csv.DictWriter(f_out, fieldnames=selected_cols)
        writer.writeheader()
        
        row_count = 0
        for row in reader:
            simplified_row = {col: row.get(col, "") for col in selected_cols}
            writer.writerow(simplified_row)
            row_count += 1

print(f"Done! Simplified database written to {output_path} with {row_count} rows and {len(selected_cols)} columns.")
