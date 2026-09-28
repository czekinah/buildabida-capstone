# Notebooks

Our Databricks notebooks, one folder per step. Each folder writes to the schema with the same number in the `buildabida-capstone` catalog.

| Order | Folder | Writes to | What it does |
| --- | --- | --- | --- |
| 0 | `00_setup` | `00-source` | Makes the catalog, the schemas and the landing volume |
| 1 | `01_bronze` | `01-bronze` | Loads each source as it came, plus the load time |
| 4 | `04_validation` | `04-validation` | Runs the checks and saves the results |
| 5 | `05_explore` | nothing | A first look at what the data says about our questions |

`run_all.py` runs steps 0, 1 and 4 in order.

## The five sources

| Notebook | Source | Table |
| --- | --- | --- |
| `01_bronze_dpwh_projects` | DPWH projects API by BetterGov.ph | `dpwh_projects` |
| `02_bronze_flood_control` | DPWH flood control map layer | `flood_control_projects` |
| `03_bronze_psgc` | PSA PSGC publication datafile | `psgc` and `population_2024` |
| `04_bronze_census_2024` | PSA 2024 census, Table B | `census_2024_table_b` |
| `05_bronze_boundaries` | Boundary maps with PSGC codes | `boundaries` |

Each load also adds a row to `01-bronze.load_log`: the source, the number of rows the source reports and the number we loaded. The checks compare the two.

## Run it

1. In your Databricks workspace, open **Workspace** and go to your home folder. Click **Create**, then **Git folder**, and paste this repo's link.
2. Open `notebooks/00_setup/00_setup_workspace` and click **Run all**. This makes the landing volume.
3. PSA blocks Databricks, so download two files by hand: the PSGC **Publication Datafile** from the [PSGC page](https://psa.gov.ph/classification/psgc) and **Table B** from the [2024 census release](https://psa.gov.ph/content/2024-census-population-popcen-population-counts-declared-official-president). In **Catalog**, open `buildabida-capstone` > `00-source` > `landing`, make a folder named `psa` and upload both files there.
4. Open `notebooks/run_all` and click **Run all**.
5. Open `notebooks/05_explore/01_explore_first_look` and click **Run all**.

Every notebook is safe to run twice. A second run replaces the tables, and the API pages from each day are kept in the landing volume.

## Each notebook should

1. Say at the top what it makes.
2. Use our `buildabida-capstone` catalog.
3. Be safe to run twice.
4. Put shared code in the `src` folder, not in the notebook.
