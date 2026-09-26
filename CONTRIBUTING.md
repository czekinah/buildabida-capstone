<img src="assets/banners/bd-strip-plan.png" alt="How we work" width="100%">

# 🤝 How we work

Short rules so five people can build one pipeline without breaking each other's work.

## 🌿 The Git flow

1. **Pull first.** Open the repo in your Databricks Git folder and pull `main` before you start.
2. **Branch.** Make a new branch named for the work.
   - `feature/raw-dpwh-projects` for new code
   - `fix/clean-dates` for a fix
   - `docs/source-cards` for docs
   - If the name is taken, add your name, like `feature/raw-dpwh-projects-bri`.
3. **Commit small.** One change per commit, with a clear message, like `Add raw load for DPWH projects`.
4. **Open a pull request** into `main`. Fill in the template and link the issue with `Closes #12`.
5. **Review.** One teammate reads it and approves. Then Kinah merges.
6. **Pull again** after a merge, so everyone stays up to date.

Never push straight to `main`.

## 🏷️ Names

| Thing | Pattern | Example |
| --- | --- | --- |
| Notebook | `NN_layer_source` | `01_raw_dpwh_projects` |
| Schema | the layer name | `raw`, `clean`, `mart`, `validation` |
| Table | `source_or_topic` in snake_case | `clean.dpwh_projects` |
| Column | snake_case, no spaces | `contract_id`, `amount_paid` |

## 🛡️ Data quality

Every table we build gets checks. We save the results in one table with the same columns every time:

| column | data_quality_check | failed_rows | total_rows | percentage | status |
| --- | --- | --- | --- | --- | --- |
| contract_id | not null | 0 | 1000 | 0.00 | PASS |

## 🔒 Keep it safe

- Never commit keys, tokens or passwords. Not even in a notebook cell.
- Do not commit data files. Data lives in Databricks tables and volumes.
- Only use sources that are public and listed in our source cards.

## 🤖 Using AI tools

Follow the 4 AI gates from our Week 10 session. They are written in the team doc.

## 🐞 Something broke?

Open an issue with the **Data bug** template. Say what you ran, what you expected and what you got.
