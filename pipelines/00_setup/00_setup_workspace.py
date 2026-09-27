# Databricks notebook source
# MAGIC %md
# MAGIC # 00 Setup workspace
# MAGIC
# MAGIC Run this once in your own Databricks Free Edition workspace.
# MAGIC
# MAGIC - **Reads:** nothing
# MAGIC - **Writes:** the schemas `bronze`, `silver`, `gold` and `validation`, and the volume `bronze.landing` for files we download by hand
# MAGIC - **Safe to run twice:** yes
# MAGIC
# MAGIC The default catalog in Free Edition is usually called `workspace`. If yours has another name, change the catalog box at the top.

# COMMAND ----------

dbutils.widgets.text("catalog", "workspace", "Catalog")
catalog = dbutils.widgets.get("catalog")
print(f"Using catalog: {catalog}")

# COMMAND ----------

layers = {
    "bronze": "Each source as it came, plus the load time",
    "silver": "Cleaned data with PSGC codes",
    "gold": "Gold marts for the dashboard and Genie",
    "validation": "Data quality results for every run",
}

for name, comment in layers.items():
    spark.sql(f"CREATE SCHEMA IF NOT EXISTS {catalog}.{name} COMMENT '{comment}'")
    print(f"Ready: {catalog}.{name}")

# COMMAND ----------

spark.sql(
    f"CREATE VOLUME IF NOT EXISTS {catalog}.bronze.landing "
    "COMMENT 'Files we download by hand, like the PSGC and census Excel files'"
)
print(f"Ready: /Volumes/{catalog}/bronze/landing")

# COMMAND ----------

display(spark.sql(f"SHOW SCHEMAS IN {catalog}"))
