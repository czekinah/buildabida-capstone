# Databricks notebook source
# MAGIC %md
# MAGIC # Flood list: the repeated contract IDs
# MAGIC
# MAGIC The flood control list has 9,855 rows but only 9,698 contract IDs, so 157 rows repeat an ID. Before silver drops any row, this notebook checks what the repeats are (D-19). It reads only `01-bronze`.`flood_control_projects` and saves nothing.
# MAGIC
# MAGIC What we found on Sep 29:
# MAGIC
# MAGIC - None of the repeats are copies. Every repeated row has at least one field that is different.
# MAGIC - Most are different parts of one contract. Each part has its own project ID and component ID, and most have their own cost and map point.
# MAGIC - The rest are one part split by funding year, with the same cost on each row.
# MAGIC - So bronze keeps every row. When all the rows of a contract show the same cost, silver should count that cost once.

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. What kind of repeat is each contract ID?

# COMMAND ----------

# MAGIC %sql
# MAGIC WITH repeated AS (
# MAGIC     SELECT
# MAGIC         contract_id,
# MAGIC         COUNT(*)                     AS rows_in_list,
# MAGIC         COUNT(DISTINCT component_id)  AS parts,
# MAGIC         COUNT(DISTINCT CONCAT_WS('|', CAST(infra_year AS STRING), CAST(funding_year AS STRING))) AS years,
# MAGIC         COUNT(DISTINCT contract_cost) AS costs,
# MAGIC         MAX(contract_cost)            AS cost
# MAGIC     FROM `buildabida-capstone`.`01-bronze`.flood_control_projects
# MAGIC     GROUP BY contract_id
# MAGIC     HAVING COUNT(*) > 1
# MAGIC )
# MAGIC SELECT
# MAGIC     CASE
# MAGIC         WHEN parts > 1 AND costs > 1 THEN 'Different parts, each with its own cost'
# MAGIC         WHEN parts > 1 THEN 'Different parts, same cost on every row'
# MAGIC         WHEN years > 1 THEN 'One part, split by funding year'
# MAGIC         ELSE 'One part, same year'
# MAGIC     END                   AS kind_of_repeat,
# MAGIC     COUNT(*)              AS contract_ids,
# MAGIC     SUM(rows_in_list - 1) AS extra_rows,
# MAGIC     ROUND(SUM(IF(costs = 1, (rows_in_list - 1) * cost, 0)) / 1e9, 2) AS cost_counted_twice_billion_pesos
# MAGIC FROM repeated
# MAGIC GROUP BY 1
# MAGIC ORDER BY contract_ids DESC

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. The repeated rows, side by side
# MAGIC
# MAGIC Look at a few to see the parts. The map point and the component description usually change from row to row.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT contract_id, project_id, component_id, infra_year, funding_year, contract_cost, latitude, longitude, component_description
# MAGIC FROM `buildabida-capstone`.`01-bronze`.flood_control_projects
# MAGIC WHERE contract_id IN (
# MAGIC     SELECT contract_id
# MAGIC     FROM `buildabida-capstone`.`01-bronze`.flood_control_projects
# MAGIC     GROUP BY contract_id
# MAGIC     HAVING COUNT(*) > 1
# MAGIC )
# MAGIC ORDER BY contract_id, component_id, funding_year
