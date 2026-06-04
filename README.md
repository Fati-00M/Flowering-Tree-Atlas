# Flowering Tree Atlas 🌸🌳

A comprehensive, curated database of global flowering trees. This project consolidates botanical taxonomy with native regional distributions, climate parameters (dominant biomes and moisture indices), functional TRY traits, and economic plant uses.

The repository includes automation scripts to clean, align, deduplicate, and merge multiple independent datasets into a unified research database.

---

## 🚀 Key Features

* **Unified Database**: Consolidates 5 independent raw datasets covering global distribution, traits, uses, and climate envelopes.
* **Intelligent Deduplication**: Merges duplicate records (e.g., trees with multiple recorded economic uses like `Medicines` and `Poisons`) into unified entries using structured text concatenation.
* **Simplified Dataset**: Includes a lightweight, easy-to-read version (`flowering_trees_simplified.csv`) containing only key analytical columns.
* **Pre-filtered Taxonomy**: Standardized using World Flora Online (WFO) taxon identifiers to ensure clean matching across all datasets.

---

## 📁 Repository Structure

```text
├── Flowering-Tree-Atlas/
│   ├── Flowering Trees/                    # Raw WFO taxonomic reference databases (Git-ignored)
│   ├── Flowering Trees Climate/            # Envelopes (Biome & Climatic Moisture Index)
│   ├── Flowering Trees Countries/          # Native ranges and regional distributions
│   ├── Flowering Trees TRY Traits/         # TRY plant functional trait matrix
│   ├── Flowering Trees Uses/               # Economic botany and plant uses
│   │
│   ├── merge_databases.py                  # Script to compile the main database
│   ├── generate_simplified_csv.py          # Script to extract the simplified dataset
│   │
│   ├── flowering_trees_combined.csv        # Unified Database (53,477 rows × 66 cols)
│   ├── flowering_trees_simplified.csv      # Simplified Database (53,477 rows × 27 cols)
│   │
│   ├── .gitignore                          # Standard ignores and exclusions for large files (>50MB)
│   └── README.md                           # Project documentation
```

---

## 🛠️ Setup & Usage

### Prerequisites
All operations require a Python environment with standard libraries. You can use the active conda environment:
```bash
conda activate flowering-trees
```

### 1. Build the Main Combined Database
Run `merge_databases.py` to align all 5 datasets by `taxonid`, combine base taxonomy, merge duplicate records in the uses dataset, and write the output:
```bash
python merge_databases.py
```
* **Output**: `flowering_trees_combined.csv` (contains all 66 columns).

### 2. Generate the Simplified Version
Run `generate_simplified_csv.py` to extract only the key analytical columns (removing detailed taxonomy and raw climate statistics):
```bash
python generate_simplified_csv.py
```
* **Output**: `flowering_trees_simplified.csv` (contains 27 essential columns).

---

## 📊 Database Schema (Simplified Version)

The simplified version of the database (`flowering_trees_simplified.csv`) includes **53,477 rows** representing unique tree species with the following columns:

| Category | Column Names | Description |
| :--- | :--- | :--- |
| **Taxonomy** | `scientificname` | Standardized botanical name |
| **Climate Envelopes** | `dominant biome`<br>`dominant climatic moisture index` | Dominant global biome and CMI values for the species |
| **TRY Traits** | `flower color`, `flower sex`, `fruit type`, `plant growth form`, `plant height`, `plant lifespan (longevity)`, `plant lifespan: age trees reach in forested stands`, `plant woodiness`, `wood growth ring distinction`, etc. | 20 selected vegetative, seed, and reproductive traits |
| **Economic Uses** | `Category of Use`<br>`Crop Wild Relative` | Human uses (e.g., *Materials; Medicines; Poisons*) and crop relative status |
| **Regions** | `native to`<br>`native range` | Native countries and geographical regions |
