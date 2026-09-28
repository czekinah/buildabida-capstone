# Databricks notebook source
# MAGIC %md
# MAGIC # Set up the catalog
# MAGIC
# MAGIC Run this once in your own workspace. It is safe to run again.
# MAGIC
# MAGIC - **Makes:** the `buildabida` catalog, the `bronze`, `silver`, `gold` and `validation` schemas, and the `bronze.landing` volume
# MAGIC - **Names come from:** `buildabida/config.py`

# COMMAND ----------

from buildabida import config

dbutils.widgets.text("catalog", config.CATALOG)
catalog = dbutils.widgets.get("catalog")

spark.sql(f"CREATE CATALOG IF NOT EXISTS {catalog}")
for schema, comment in config.SCHEMAS.items():
    spark.sql(f"CREATE SCHEMA IF NOT EXISTS {catalog}.{schema} COMMENT '{comment}'")
volume = f"{catalog}.{config.LANDING_VOLUME}"
spark.sql(f"CREATE VOLUME IF NOT EXISTS {volume} COMMENT 'Files we download by hand'")

display(spark.sql(f"SHOW SCHEMAS IN {catalog}"))
