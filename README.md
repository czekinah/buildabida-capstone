<p align="center">
  <img src="assets/banners/github-readme.png" alt="Buildabida. Every project. Every peso. Every place." width="100%">
</p>

# Infrastructure Project Monitoring Pipeline

This project tracks public works projects in the Philippines, from the source data to a dashboard. It joins DPWH project records with official place codes (PSGC) and the 2024 census. This lets us see where project money goes, how far each project has gone, and how that compares with the number of people in each place.

Built by team Buildabida (LT2) for the FTW Foundation Data Engineering Track capstone, 2026.

> **Status:** Planning. The schema is due on Oct 3, 2026. The run steps below are filled in as each layer is built.

## Who it is for

- People who want to check public works spending in their province or city
- Planners who want to find places with many people but few projects
- Our mentor, support instructor and judges, who need to run and check the pipeline

## Questions

Our main question is a draft. We will confirm it with our mentor before Oct 3.

**Main question:** Where does public works money go, and does it reach the places with the most people?

1. How much project money went to each region and province, in total and per person?
2. Which projects are late or not moving?
3. Does the amount paid match the reported progress?
4. How do flood control projects compare with other project types?
5. Which places have many people but few projects?

## How it works

```mermaid
flowchart LR
    S["Sources<br>DPWH projects, flood control,<br>PSGC, census, maps"]:::src --> R["raw"]:::raw
    R --> C["clean"]:::clean
    C --> M["mart"]:::mart
    M --> D["Dashboard"]:::dash
    C -.-> V["validation"]:::val
    M -.-> V
    classDef src fill:#D7E8FF,stroke:#2B2A4C,color:#2B2A4C
    classDef raw fill:#FFDCC8,stroke:#2B2A4C,color:#2B2A4C
    classDef clean fill:#D2F4E4,stroke:#2B2A4C,color:#2B2A4C
    classDef mart fill:#FFF2BF,stroke:#2B2A4C,color:#2B2A4C
    classDef val fill:#E6DDFF,stroke:#2B2A4C,color:#2B2A4C
    classDef dash fill:#FFD9E6,stroke:#2B2A4C,color:#2B2A4C
```

| Layer | What it does |
| --- | --- |
| raw | Keeps each source as it came, plus the load time. No changes. |
| clean | Fixes types and dates, removes duplicates, and gives every project a PSGC code. |
| mart | Holds the facts and dimensions that the dashboard reads. |
| validation | Saves the result of every check. A failed critical check stops the run. |

## Data sources

| Source | What we use it for |
| --- | --- |
| [DPWH projects API](https://api.dpwh.bettergov.ph/projects) by BetterGov.ph | Every DPWH project with budget, amount paid, progress, dates, contractor and map point. About 265,000 projects as of Sep 2026. |
| [DPWH Transparency Portal](https://transparency.dpwh.gov.ph) | The official source. We use it to spot-check the API. |
| [Sumbong sa Pangulo](https://sumbongsapangulo.ph) | Flood control projects |
| [PSGC 2Q 2026](https://psa.gov.ph/classification/psgc) by PSA | Official codes for 18 regions, 82 provinces, 149 cities, 1,493 towns and 42,010 barangays |
| [2024 Census of Population](https://psa.gov.ph) by PSA | Population of each place |
| [Boundary maps](https://data.humdata.org/dataset/cod-ab-phl) on HDX | Matching each project's map point to a place |

Notes on the sources:

- In the API, `location.province` holds a DPWH district office name, like `Albay 2nd DEO`. It is not a PSGC province. We use the map point and the boundary maps to find the real place.
- Some projects may appear in both the DPWH list and the flood control list. We match them by contract ID so we do not count them twice.

## Data model (draft)

The final schema is due on Oct 3. This is our starting point.

| Table | One row is | Key |
| --- | --- | --- |
| `raw.dpwh_projects` | One project, as the API returns it | `contract_id` |
| `raw.flood_control_projects` | One flood control project | `contract_id` |
| `raw.psgc` | One place in the PSGC list | `psgc_code` |
| `raw.population_2024` | One place and its 2024 population | `psgc_code` |
| `clean.projects` | One project from any source, with a PSGC code | `contract_id` |
| `mart.dim_place` | One region, province, city or town | `psgc_code` |
| `mart.dim_project_type` | One project type | `project_type_id` |
| `mart.fact_project` | One project | `contract_id` |
| `validation.dq_results` | One check on one column in one run | `run_id`, `table_name`, `column_name`, `check_name` |

## How to run

The full run order is added when the first notebooks are merged.

### Requirements

- A Databricks Free Edition account
- Read access to this repo
- Databricks access to the source links above. See [Known limits](#known-limits).

### Setup

1. In Databricks, open **Workspace** and go to your home folder.
2. Click **Create**, then **Git folder**.
3. Paste `https://github.com/czekinah/buildabida-capstone.git` and click **Create Git folder**.
4. Before you run anything, click the branch name and then **Pull**.

### Run order

| Step | Folder | What it does | Status |
| --- | --- | --- | --- |
| 1 | `pipelines/01_raw` | Loads each source into `raw` | Planned |
| 2 | `pipelines/02_clean` | Builds `clean` tables and adds PSGC codes | Planned |
| 3 | `pipelines/03_mart` | Builds the facts and dimensions | Planned |
| 4 | `pipelines/04_validation` | Runs all checks and saves the results | Planned |

## Validation

Every run checks the data before it moves to the next layer.

| Check | Example | If it fails |
| --- | --- | --- |
| Not null | `contract_id` is never empty | Stop the run |
| Unique | One row per `contract_id` in `clean.projects` | Stop the run |
| Row counts | Raw, clean and mart totals match, after known drops | Stop the run |
| Valid range | `progress` is from 0 to 100 | Flag the row |
| Map point | The point is inside the Philippines | Flag the row |
| Place match | Every project has a PSGC code | Flag and report the match rate |
| Money | `amount_paid` is not more than `budget` | Flag the row |

Results go to `validation.dq_results` with the same columns we used in Week 9: `column`, `data_quality_check`, `failed_rows`, `total_rows`, `percentage` and `status`.

A GitHub Actions check also looks for broken links in our Markdown files on every pull request.

## Decisions

We log each decision with an ID, the options we looked at, and why we picked one. Open decisions right now:

| ID | Question |
| --- | --- |
| D-01 | Which Databricks workspace runs the final pipeline and dashboard? |
| D-02 | What is our final main question? |
| D-03 | How do we match a project to a place: map point, office name, or both? |
| D-04 | How do we handle projects that are in both the DPWH and flood control lists? |

## Known limits

- Databricks Free Edition only lets notebooks reach trusted websites. If a source is blocked, we download the file and upload it to a Databricks volume, and we note the download date.
- Each of us has our own Free Edition workspace. We share code through this repo, not through one workspace.

## Repo structure

```
.
├── README.md          this file
├── CONTRIBUTING.md    how we branch, review and merge
├── assets/banners/    team images
├── pipelines/         Databricks notebooks, one folder per layer
├── docs/              source cards, schema, data model and decisions
└── .github/           issue and pull request templates, and checks
```

## Team and timeline

Kinah (lead), Bri, Nadine, Sam and Tricia. Mentor: Carmi. Support instructor: Simonee.

Tasks are GitHub issues, and the project board shows who is working on what. Every change goes through a pull request with one review. See [CONTRIBUTING.md](CONTRIBUTING.md).

| Date | Milestone |
| --- | --- |
| Oct 3 | Source cards and schema |
| Oct 10 | Clean and mart tables pass their checks |
| Oct 17 | Dashboard, cert exam and judged presentation |
| Oct 24 | Graduation. Final README and docs. |
