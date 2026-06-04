import csv
import os

base_dir = r"d:\Climate Change data\FLOWERING TREES PROJECT"

files = {
    "biome": os.path.join(base_dir, "Flowering Trees Climate", "flowering_trees_dominant_biome.csv"),
    "cmi": os.path.join(base_dir, "Flowering Trees Climate", "flowering_trees_dominant_CMI.csv"),
    "countries": os.path.join(base_dir, "Flowering Trees Countries", "flowering_trees_native_range.csv"),
    "traits": os.path.join(base_dir, "Flowering Trees TRY Traits", "flowering_trees_traits.csv"),
    "uses": os.path.join(base_dir, "Flowering Trees Uses", "flowering_trees_uses.csv")
}

output_path = os.path.join(base_dir, "flowering_trees_combined.csv")

# We will read each file.
# Since taxonid is unique for each species, we'll index the records by taxonid.
# We will preserve the order of taxonid as seen in the first file (biome).

taxonomy_cols = [
    'taxonid', 'scientificnameid', 'localid', 'scientificname', 'taxonrank',
    'parentnameusageid', 'scientificnameauthorship', 'family', 'subfamily',
    'tribe', 'subtribe', 'genus', 'subgenus', 'specificepithet',
    'infraspecificepithet', 'verbatimtaxonrank', 'nomenclaturalstatus',
    'namepublishedin', 'taxonomicstatus', 'acceptednameusageid',
    'originalnameusageid', 'nameaccordingtoid', 'taxonremarks', 'created',
    'modified', 'references', 'source', 'majorgroup', 'tplid'
]

# Specific columns for each file:
biome_cols = ['Tmo10_n', 'Tmo10_Q05', 'Tmo10_Q95', 'Biome', 'dominant biome']
cmi_cols = ['n', 'Q05', 'Q95', 'climatic moisture index', 'dominant climatic moisture index']
countries_cols = ['native to', 'native_match', 'native range']
traits_cols = [
    'speciesname', 'flower color', 'flower sex',
    'flowering lag time: number of days from exposition start to flowering',
    'flowering requirement (requirement for fertility)', 'fruit type',
    'plant flowering', 'plant growth form', 'plant growth temperature range',
    'plant height', 'plant human usage types', 'plant lifespan (longevity)',
    'plant lifespan: age trees reach in forested stands', 'plant woodiness',
    'seed germination base temperature', 'seed germination base water potential',
    'seed germination lag time', 'seed germination requirement',
    'seed germination temperature', 'seed germination type',
    'wood growth ring distinction'
]
uses_cols = ['Category of Use', 'Crop Wild Relative', 'Source']

# Combine all columns
final_header = taxonomy_cols + biome_cols + cmi_cols + countries_cols + traits_cols + uses_cols

# We will read biome first to get the main taxonomy details and row order.
taxon_order = []
db = {}

# Load biome
print("Loading biome file...")
with open(files["biome"], "r", encoding="utf-8", errors="replace") as f:
    reader = csv.DictReader(f)
    for row in reader:
        taxonid = row["taxonid"]
        taxon_order.append(taxonid)
        # Store base taxonomy
        db[taxonid] = {col: row.get(col, "") for col in taxonomy_cols}
        # Add biome columns
        for col in biome_cols:
            db[taxonid][col] = row.get(col, "")

# Load CMI
print("Loading CMI file...")
with open(files["cmi"], "r", encoding="utf-8", errors="replace") as f:
    reader = csv.DictReader(f)
    for row in reader:
        taxonid = row["taxonid"]
        if taxonid not in db:
            print(f"Warning: taxonid {taxonid} from CMI not in base db!")
            db[taxonid] = {col: "" for col in taxonomy_cols}
        for col in cmi_cols:
            db[taxonid][col] = row.get(col, "")

# Load countries
print("Loading countries file...")
with open(files["countries"], "r", encoding="utf-8", errors="replace") as f:
    reader = csv.DictReader(f)
    for row in reader:
        taxonid = row["taxonid"]
        if taxonid not in db:
            print(f"Warning: taxonid {taxonid} from countries not in base db!")
            db[taxonid] = {col: "" for col in taxonomy_cols}
        for col in countries_cols:
            db[taxonid][col] = row.get(col, "")

# Load traits
print("Loading traits file...")
with open(files["traits"], "r", encoding="utf-8", errors="replace") as f:
    reader = csv.DictReader(f)
    for row in reader:
        taxonid = row["taxonid"]
        if taxonid not in db:
            print(f"Warning: taxonid {taxonid} from traits not in base db!")
            db[taxonid] = {col: "" for col in taxonomy_cols}
        for col in traits_cols:
            db[taxonid][col] = row.get(col, "")

# Load uses (handling potential duplicates)
print("Loading uses file...")
uses_data = {} # taxonid -> list of rows
with open(files["uses"], "r", encoding="utf-8", errors="replace") as f:
    reader = csv.DictReader(f)
    for row in reader:
        taxonid = row["taxonid"]
        if taxonid not in uses_data:
            uses_data[taxonid] = []
        uses_data[taxonid].append(row)

# Merge uses data into db
print("Merging uses data...")
for taxonid, rows in uses_data.items():
    if taxonid not in db:
        print(f"Warning: taxonid {taxonid} from uses not in base db!")
        db[taxonid] = {col: "" for col in taxonomy_cols}
    
    # If there is only one row, just map columns
    if len(rows) == 1:
        for col in uses_cols:
            db[taxonid][col] = rows[0].get(col, "")
    else:
        # Merge duplicate rows
        # For each column in uses_cols, collect unique non-empty values
        for col in uses_cols:
            values = []
            for r in rows:
                val = r.get(col, "").strip()
                if val and val not in values:
                    values.append(val)
            # Combine values
            db[taxonid][col] = "; ".join(values)

# Write output file
print(f"Writing output to {output_path}...")
with open(output_path, "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=final_header)
    writer.writeheader()
    for taxonid in taxon_order:
        # Fill missing keys in db in case any are missing (though we initialized from biome)
        row_data = db[taxonid]
        # Make sure every header field is present
        complete_row = {col: row_data.get(col, "") for col in final_header}
        writer.writerow(complete_row)

print("Done! Combined database successfully generated.")
