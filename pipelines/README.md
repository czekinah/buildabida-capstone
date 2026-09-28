# Pipelines

Our Databricks notebooks, one folder per step. Run the folders in this order.

| Order | Folder | What it does |
| --- | --- | --- |
| 0 | `00_setup` | Makes the catalog, schemas and landing volume, and checks our sources |
| 1 | `01_bronze` | Loads each source as it came into `bronze` |
| 2 | `02_silver` | Fixes types, removes duplicates and adds PSGC codes |
| 3 | `03_gold` | Builds the facts and dimensions for the dashboard and Genie |
| 4 | `04_validation` | Runs the checks and saves the results |

We add each folder with its first notebook.

## Shared code

Names and links live in [`buildabida/config.py`](../buildabida/config.py). Helpers live next to it. Import them at the top of a notebook:

```python
from buildabida import api, config
```

This works because Databricks adds the repo folder to the Python path. Don't copy a name or a link into a notebook. Change it in `config.py`, and every notebook gets the change.

## Notebook names

Use `NN_layer_source`, like `01_bronze_dpwh_projects` or `02_silver_psgc`. The number sets the run order in a folder.

## Each notebook should

1. Say at the top what it makes and where its names come from.
2. Import the catalog, schema and source names from `buildabida/config.py`.
3. Be safe to run twice. A second run with the same input adds no duplicate rows.
4. End with its data quality checks.
5. Say in a comment if AI helped write it, and what you checked.

## Code checks

Ruff checks our Python code on every pull request. If it finds a problem, the pull request shows a red X and the details. Fix the line it names, then commit again.
