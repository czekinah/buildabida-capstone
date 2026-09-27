# Databricks notebook source
# MAGIC %md
# MAGIC # 01 Check sources
# MAGIC
# MAGIC Free Edition only lets code reach some websites. This notebook checks each of our sources.
# MAGIC
# MAGIC - **Reads:** one small request to each source
# MAGIC - **Writes:** nothing
# MAGIC - **If a source says BLOCKED:** download the file by hand, upload it to `/Volumes/<catalog>/bronze/landing`, and write the download date in its source card

# COMMAND ----------

import requests

SOURCES = {
    "DPWH projects API (BetterGov)": "https://api.dpwh.bettergov.ph/projects?page=1&limit=1",
    "Flood control map layer (DPWH)": "https://services1.arcgis.com/IwZZTMxZCmAmFYvF/arcgis/rest/services/FloodControl_Data_20250802_v6_corrected_coordinates_for_uploading/FeatureServer/0/query?where=1%3D1&returnCountOnly=true&f=json",
    "BetterGov open data portal": "https://data.bettergov.ph/api/v1/stats",
    "PSA PSGC page": "https://psa.gov.ph/classification/psgc",
    "PSA OpenSTAT": "https://openstat.psa.gov.ph/",
    "HDX boundary maps": "https://data.humdata.org/dataset/cod-ab-phl",
    "Hugging Face (BetterGov copies)": "https://huggingface.co/api/datasets/bettergovph/dpwh-transparency-data",
    "GitHub raw files": "https://raw.githubusercontent.com/czekinah/buildabida-capstone/main/README.md",
}

rows = []
for name, url in SOURCES.items():
    try:
        r = requests.get(url, timeout=20, headers={"User-Agent": "buildabida-capstone source check"})
        status = "OK" if r.status_code < 400 else f"HTTP {r.status_code}"
    except Exception as e:
        status = f"BLOCKED ({type(e).__name__})"
    rows.append((name, status, url))
    print(f"{status:32} {name}")

# COMMAND ----------

display(spark.createDataFrame(rows, "source string, status string, url string"))
