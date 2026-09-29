# Databricks notebook source
# MAGIC %md
# MAGIC # First look: what the bronze data says about our questions
# MAGIC
# MAGIC A first pass, before silver. It reads only `01-bronze` tables, so every number here traces back to a source. It only checks if the data can answer our questions. The real answers come from silver and gold.
# MAGIC
# MAGIC | Question | Section |
# MAGIC | --- | --- |
# MAGIC | 1. How much project money went to each region and province, in total and per person? | 2, 8 |
# MAGIC | 2. Which projects are late or not moving? | 5 |
# MAGIC | 3. Does the amount paid match the reported progress? | 6 |
# MAGIC | 4. How do flood control projects compare with other project types? | 3, 4, 7 |
# MAGIC | 5. Which places have many people but few projects? | 2, 8 |
# MAGIC | 6. What types of infrastructure get funded? | 4 |
# MAGIC
# MAGIC Money is the `budget` column: DPWH projects from 2016 to 2026, all statuses. Per person uses the 2024 census count in the PSGC file. Silver will use census Table C (D-18).
# MAGIC
# MAGIC Limits of a first pass: BARMM has no DPWH projects here, because the Bangsamoro government builds its own. Province numbers use the map point, and about 1 in 5 projects has none.

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Project types
# MAGIC
# MAGIC The `category` column is messy: many rows hold a funding code like `GAA 2025 SSP` instead of a type. So we read the type from the description. The first rule that matches wins, in the order below. Every section uses this view.

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TEMP VIEW project_types AS
# MAGIC SELECT *,
# MAGIC     CASE
# MAGIC         WHEN UPPER(description) RLIKE 'FLOOD|DRAINAGE|REVETMENT|DIKE\\b|SEAWALL|SEA WALL|RIVER CONTROL|SLOPE PROTECTION|CREEK|ESTERO' THEN 'Flood control'
# MAGIC         WHEN UPPER(description) RLIKE 'BRIDGE' THEN 'Bridge'
# MAGIC         WHEN UPPER(description) RLIKE 'HOSPITAL|HEALTH|\\bRHU\\b|\\bBHS\\b|MEDICAL|CLINIC|INFIRMARY|DIALYSIS|LYING-IN|BIRTHING' THEN 'Health'
# MAGIC         WHEN UPPER(description) RLIKE 'SCHOOL|CLASSROOM|\\bE/?S\\b|\\bNHS\\b|\\bCES\\b|ELEMENTARY|DEPED|BEFF|UNIVERSITY|STATE COLLEGE|\\bSUC\\b|ACADEMY|LEARNING CENTER' THEN 'School'
# MAGIC         WHEN UPPER(description) RLIKE 'WATER SUPPLY|WATER SYSTEM|RAIN ?WATER|CISTERN|IRRIGATION|POTABLE|SPRING DEVELOPMENT|DEEP ?WELL' THEN 'Water'
# MAGIC         WHEN UPPER(description) RLIKE 'FARM[- ]?TO[- ]?MARKET|\\bFMR\\b' THEN 'Farm-to-market road'
# MAGIC         WHEN UPPER(description) RLIKE 'ROAD|HIGHWAY|STREET|BYPASS|BY-PASS|DIVERSION|ASPHALT|PAVEMENT|CONCRETING|FLYOVER|INTERCHANGE|EXPRESSWAY|ACCESS' THEN 'Road'
# MAGIC         WHEN UPPER(description) RLIKE 'EVACUATION' THEN 'Evacuation center'
# MAGIC         WHEN UPPER(description) RLIKE 'MULTI-?PURPOSE|COVERED COURT|GYM|COMMUNITY CENTER|BARANGAY HALL|SENIOR CITIZEN|DAY ?CARE|CHILD DEVELOPMENT|PLAZA' THEN 'Multi-purpose and community'
# MAGIC         WHEN UPPER(description) RLIKE 'OFFICE BUILDING|GOVERNMENT CENTER|MUNICIPAL HALL|CITY HALL|CAPITOL|POLICE|FIRE STATION|\\bBFP\\b|\\bPNP\\b|JAIL|HALL OF JUSTICE|COURT' THEN 'Government office'
# MAGIC         WHEN UPPER(description) RLIKE 'MARKET|SLAUGHTER|FISH ?PORT|PORT\\b|WHARF|PIER|TERMINAL|TOURISM|TOURIST|AIRPORT|LIGHTHOUSE' THEN 'Port, market and tourism'
# MAGIC         WHEN UPPER(description) RLIKE 'SPORTS|STADIUM|OVAL' THEN 'Sports'
# MAGIC         WHEN UPPER(description) RLIKE 'BUILDING|FACILIT|CENTER|HALL' THEN 'Other building'
# MAGIC         ELSE 'Other'
# MAGIC     END AS project_type
# MAGIC FROM `buildabida-capstone`.`01-bronze`.dpwh_projects

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Money per region and per person

# COMMAND ----------

# MAGIC %sql
# MAGIC WITH region_names (dpwh_region, census_region) AS (
# MAGIC     VALUES
# MAGIC         ('National Capital Region', 'NATIONAL CAPITAL REGION (NCR)'),
# MAGIC         ('Cordillera Administrative Region', 'CORDILLERA ADMINISTRATIVE REGION (CAR)'),
# MAGIC         ('Region I', 'REGION I (ILOCOS REGION)'),
# MAGIC         ('Region II', 'REGION II (CAGAYAN VALLEY)'),
# MAGIC         ('Region III', 'REGION III (CENTRAL LUZON)'),
# MAGIC         ('Region IV-A', 'REGION IV-A (CALABARZON)'),
# MAGIC         ('MIMAROPA Region', 'MIMAROPA REGION'),
# MAGIC         ('Region IV-B', 'MIMAROPA REGION'),
# MAGIC         ('Region V', 'REGION V (BICOL REGION)'),
# MAGIC         ('Region VI', 'REGION VI (WESTERN VISAYAS)'),
# MAGIC         ('Negros Island Region', 'NEGROS ISLAND REGION (NIR)'),
# MAGIC         ('Region VII', 'REGION VII (CENTRAL VISAYAS)'),
# MAGIC         ('Region VIII', 'REGION VIII (EASTERN VISAYAS)'),
# MAGIC         ('Region IX', 'REGION IX (ZAMBOANGA PENINSULA)'),
# MAGIC         ('Region X', 'REGION X (NORTHERN MINDANAO)'),
# MAGIC         ('Region XI', 'REGION XI (DAVAO REGION)'),
# MAGIC         ('Region XII', 'REGION XII (SOCCSKSARGEN)'),
# MAGIC         ('Region XIII', 'REGION XIII (CARAGA)')
# MAGIC ),
# MAGIC money AS (
# MAGIC     SELECT n.census_region, COUNT(*) AS projects, SUM(t.budget) AS budget,
# MAGIC            SUM(IF(t.project_type = 'Flood control', t.budget, 0)) AS flood_budget
# MAGIC     FROM project_types AS t
# MAGIC     JOIN region_names AS n ON t.region = n.dpwh_region
# MAGIC     GROUP BY n.census_region
# MAGIC )
# MAGIC SELECT c.name AS region, c.pop_2024,
# MAGIC        COALESCE(m.projects, 0) AS projects,
# MAGIC        ROUND(COALESCE(m.budget, 0) / 1e9, 1) AS budget_billion_pesos,
# MAGIC        ROUND(COALESCE(m.budget, 0) / c.pop_2024) AS pesos_per_person,
# MAGIC        ROUND(COALESCE(m.projects, 0) * 100000 / c.pop_2024) AS projects_per_100k_people,
# MAGIC        ROUND(100 * m.flood_budget / m.budget, 1) AS flood_control_percent
# MAGIC FROM `buildabida-capstone`.`01-bronze`.census_2024_table_b AS c
# MAGIC LEFT JOIN money AS m ON m.census_region = c.name
# MAGIC WHERE c.is_region
# MAGIC ORDER BY pesos_per_person DESC

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Money per year, and the flood control share

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT infra_year,
# MAGIC        COUNT(*) AS projects,
# MAGIC        ROUND(SUM(budget) / 1e9, 1) AS budget_billion_pesos,
# MAGIC        ROUND(SUM(IF(project_type = 'Flood control', budget, 0)) / 1e9, 1) AS flood_billion_pesos,
# MAGIC        ROUND(100 * SUM(IF(project_type = 'Flood control', budget, 0)) / SUM(budget), 1) AS flood_percent
# MAGIC FROM project_types
# MAGIC GROUP BY infra_year
# MAGIC ORDER BY infra_year

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Types of infrastructure

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT project_type,
# MAGIC        COUNT(*) AS projects,
# MAGIC        ROUND(SUM(budget) / 1e9, 1) AS budget_billion_pesos,
# MAGIC        ROUND(100 * SUM(budget) / SUM(SUM(budget)) OVER (), 1) AS percent_of_money,
# MAGIC        ROUND(100 * COUNT_IF(status = 'Completed') / COUNT(*), 1) AS percent_completed
# MAGIC FROM project_types
# MAGIC GROUP BY project_type
# MAGIC ORDER BY budget_billion_pesos DESC

# COMMAND ----------

# MAGIC %md
# MAGIC ## 5. Projects that are not moving
# MAGIC
# MAGIC The API has no target date for projects that are still going, so we can't count late projects directly. These are the signs we can see.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT 'On-going, started more than 2 years ago' AS sign, COUNT(*) AS projects, ROUND(SUM(budget) / 1e9, 1) AS budget_billion_pesos
# MAGIC FROM project_types
# MAGIC WHERE status = 'On-Going' AND start_date < ADD_MONTHS(CURRENT_DATE(), -24)
# MAGIC UNION ALL
# MAGIC SELECT 'On-going, started before 2022', COUNT(*), ROUND(SUM(budget) / 1e9, 1)
# MAGIC FROM project_types
# MAGIC WHERE status = 'On-Going' AND start_date < DATE'2022-01-01'
# MAGIC UNION ALL
# MAGIC SELECT 'On-going, still at 0 percent', COUNT(*), ROUND(SUM(budget) / 1e9, 1)
# MAGIC FROM project_types
# MAGIC WHERE status = 'On-Going' AND progress = 0
# MAGIC UNION ALL
# MAGIC SELECT 'For procurement, from 2024 or earlier', COUNT(*), ROUND(SUM(budget) / 1e9, 1)
# MAGIC FROM project_types
# MAGIC WHERE status = 'For Procurement' AND infra_year <= 2024
# MAGIC UNION ALL
# MAGIC SELECT 'Terminated', COUNT(*), ROUND(SUM(budget) / 1e9, 1)
# MAGIC FROM project_types
# MAGIC WHERE status = 'Terminated'

# COMMAND ----------

# MAGIC %md
# MAGIC ## 6. Amount paid against progress

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT COUNT(*) AS projects,
# MAGIC        COUNT_IF(amount_paid > 0) AS with_amount_paid,
# MAGIC        COUNT_IF(status = 'Completed') AS completed,
# MAGIC        COUNT_IF(status = 'Completed' AND COALESCE(amount_paid, 0) = 0) AS completed_but_paid_zero
# MAGIC FROM project_types

# COMMAND ----------

# MAGIC %md
# MAGIC ## 7. The flood control list against the DPWH list, and the biggest contractors

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT COUNT(*) AS flood_rows,
# MAGIC        COUNT(DISTINCT f.contract_id) AS contracts,
# MAGIC        COUNT(p.contract_id) AS rows_found_in_dpwh_list,
# MAGIC        COUNT_IF(ABS(p.budget - f.contract_cost) < 1) AS dpwh_budget_equals_contract_cost,
# MAGIC        COUNT_IF(ABS(p.budget - f.abc) < 1) AS dpwh_budget_equals_abc,
# MAGIC        COUNT_IF(p.status = 'Completed') AS completed_in_dpwh_list,
# MAGIC        ROUND(SUM(f.contract_cost) / 1e9, 1) AS contract_cost_billion_pesos,
# MAGIC        COUNT_IF(f.type_of_work = 'Construction of Flood Mitigation Structure') AS only_general_label
# MAGIC FROM `buildabida-capstone`.`01-bronze`.flood_control_projects AS f
# MAGIC LEFT JOIN `buildabida-capstone`.`01-bronze`.dpwh_projects AS p ON p.contract_id = f.contract_id

# COMMAND ----------

# MAGIC %sql
# MAGIC WITH by_contractor AS (
# MAGIC     SELECT contractor, COUNT(*) AS projects, SUM(budget) AS budget
# MAGIC     FROM project_types
# MAGIC     WHERE budget > 0
# MAGIC     GROUP BY contractor
# MAGIC )
# MAGIC SELECT contractor, projects, ROUND(budget / 1e9, 1) AS budget_billion_pesos,
# MAGIC        ROUND(100 * budget / SUM(budget) OVER (), 2) AS percent_of_money
# MAGIC FROM by_contractor
# MAGIC ORDER BY budget DESC
# MAGIC LIMIT 15

# COMMAND ----------

# MAGIC %md
# MAGIC ## 8. Money per person in each province and city
# MAGIC
# MAGIC Each project's map point is matched to a city shape first, then a province shape. Cities come first, because a highly urbanized city sits inside its province's shape but has its own population count. Silver will do this properly for every barangay (issue #16).

# COMMAND ----------

import sys

sys.path.append("../..")  # the repo root, so the import below works everywhere

from src import places

shapes = (
    spark.table("`buildabida-capstone`.`01-bronze`.boundaries")
    .where("boundary_class IN ('highly_urbanized_cities', 'provinces')")
    .orderBy("boundary_class")  # highly_urbanized_cities sorts before provinces
    .select("psgc_name", "geometry_json")
    .collect()
)
points = spark.sql("""
    SELECT contract_id, longitude, latitude
    FROM `buildabida-capstone`.`01-bronze`.dpwh_projects
    WHERE latitude IS NOT NULL AND longitude IS NOT NULL
""").toPandas()
points["place"] = places.assign(points["longitude"], points["latitude"], [(s[0], s[1]) for s in shapes])
spark.createDataFrame(points[["contract_id", "place"]]).createOrReplaceTempView("project_place")
print(f"{points['place'].notna().sum():,} of {len(points):,} map points fall inside a province or city shape.")

# COMMAND ----------

# MAGIC %sql
# MAGIC WITH money AS (
# MAGIC     SELECT UPPER(pp.place) AS place, COUNT(*) AS projects, SUM(t.budget) AS budget,
# MAGIC            SUM(IF(t.project_type = 'Flood control', t.budget, 0)) AS flood_budget,
# MAGIC            SUM(IF(t.project_type = 'Health', t.budget, 0)) AS health_budget
# MAGIC     FROM project_place AS pp
# MAGIC     JOIN project_types AS t USING (contract_id)
# MAGIC     WHERE pp.place IS NOT NULL
# MAGIC     GROUP BY UPPER(pp.place)
# MAGIC ),
# MAGIC people AS (
# MAGIC     SELECT UPPER(name) AS place, population_2024
# MAGIC     FROM `buildabida-capstone`.`01-bronze`.population_2024
# MAGIC     WHERE geographic_level IN ('Prov', 'City')
# MAGIC )
# MAGIC SELECT m.place, p.population_2024, m.projects,
# MAGIC        ROUND(m.budget / 1e9, 1) AS budget_billion_pesos,
# MAGIC        ROUND(m.budget / p.population_2024) AS pesos_per_person,
# MAGIC        ROUND(m.flood_budget / p.population_2024) AS flood_pesos_per_person,
# MAGIC        ROUND(m.health_budget / p.population_2024) AS health_pesos_per_person
# MAGIC FROM money AS m
# MAGIC JOIN people AS p USING (place)
# MAGIC ORDER BY pesos_per_person
