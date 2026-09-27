# Pipelines

Databricks notebooks, one folder per layer. Run them in this order.

| Order | Folder | What it does |
| --- | --- | --- |
| 1 | `01_bronze` | Loads each source as it came into the `bronze` schema |
| 2 | `02_silver` | Fixes types, removes duplicates and adds PSGC codes |
| 3 | `03_gold` | Builds the gold marts: facts and dimensions for the dashboard and Genie |
| 4 | `04_validation` | Runs the checks and saves the results |

The folders are added with the first notebook for each layer.

## Notebook names

Use `NN_layer_source`, like `01_bronze_dpwh_projects` or `02_silver_psgc`. The number sets the run order inside a folder.

## Each notebook should

1. Say at the top what it reads, what it writes and how to run it.
2. Use widgets or a config cell for the catalog and schema names, not hard-coded names.
3. Be safe to run twice. A second run with the same input should not add duplicate rows.
4. End with its data quality checks.
5. Say in a comment if AI helped write it, and what you checked.
