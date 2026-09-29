# Databricks notebook source
# MAGIC %md
# MAGIC # Check that Databricks can reach each source
# MAGIC
# MAGIC Databricks Free Edition can only reach some websites. This notebook asks each source for a small answer and shows what came back. It saves nothing, so it is safe to run any time.
# MAGIC
# MAGIC - **200** means our code can load the source in Databricks.
# MAGIC - **403** or an error means we download the files by hand, like the PSA files.
# MAGIC
# MAGIC The last source is the DENR MGB flood susceptibility map that Nadine suggested on Sep 29. The team decides on Wed, Sep 30 if we add it (D-21).

# COMMAND ----------

import json
import sys

sys.path.append("../..")  # the repo root, so the import below works everywhere

import requests

from src import api, config

MGB_FLOOD_LAYER = (
    "https://controlmap.mgb.gov.ph/arcgis/rest/services/GeospatialDataInventory/"
    "GDI_Detailed_Flood_Susceptibility/FeatureServer/0/query"
)
COUNT_ONLY = {"where": "1=1", "returnCountOnly": "true", "f": "json"}

SOURCES = [
    ("DPWH projects API", config.DPWH_API, {"page": 1, "limit": 1}),
    ("Flood control map layer", config.FLOOD_LAYER, COUNT_ONLY),
    ("PSA PSGC page", "https://psa.gov.ph/classification/psgc", None),
    ("PSA OpenSTAT", "https://openstat.psa.gov.ph/PXWeb/api/v1/en/DB/1A/PO_2024/0231A6DPUP0.px", None),
    ("Boundary maps", config.BOUNDARY_BASE + "regions.geojson", None),
    ("MGB flood susceptibility (proposed)", MGB_FLOOD_LAYER, COUNT_ONLY),
]

# COMMAND ----------

results = []
for name, url, params in SOURCES:
    try:
        with requests.get(url, params=params, headers=api.HEADERS, timeout=60, stream=True) as response:
            answer = str(response.status_code)
    except requests.RequestException as error:
        answer = type(error).__name__
    results.append((name, answer, url))
    print(f"{answer:>20}  {name}")

display(spark.createDataFrame(results, "source string, answer string, url string"))

# COMMAND ----------

# MAGIC %md
# MAGIC ## The MGB flood map, if Databricks can reach it
# MAGIC
# MAGIC How many flood areas it has and how many have each rating: VHF is very high, HF high, MF moderate and LF low. It also downloads 20 shapes to guess how big the full map is.

# COMMAND ----------

stats = [{"statisticType": "count", "onStatisticField": "OBJECTID", "outStatisticFieldName": "areas"}]
try:
    total = api.get_json(MGB_FLOOD_LAYER, COUNT_ONLY, tries=2)["count"]
    by_rating = api.get_json(
        MGB_FLOOD_LAYER,
        {"where": "1=1", "groupByFieldsForStatistics": "FloodSusc", "outStatistics": json.dumps(stats), "f": "json"},
        tries=2,
    )["features"]
    sample = requests.get(
        MGB_FLOOD_LAYER,
        params={"where": "1=1", "outFields": "*", "returnGeometry": "true", "resultOffset": 30000, "resultRecordCount": 20, "f": "geojson"},
        headers=api.HEADERS,
        timeout=180,
    )
    sample.raise_for_status()
    size_gb = len(sample.content) / 20 * total / 1e9
    print(f"{total:,} flood areas. The full map is about {size_gb:.1f} GB as GeoJSON, from a sample of 20 shapes.")
    ratings = [(row["attributes"]["FloodSusc"], row["attributes"]["areas"]) for row in by_rating]
    display(spark.createDataFrame(ratings, "rating string, areas long"))
except (requests.RequestException, ValueError, KeyError) as error:
    print("Databricks cannot reach the MGB map:", type(error).__name__)
