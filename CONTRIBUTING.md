# How we work

These rules help five people build one pipeline without breaking each other's work.

## Before you start

1. Send Kinah your GitHub username so she can add you to the repo.
2. In Databricks, open **Settings**, then **Linked accounts**, and link your GitHub account. This lets you commit from Databricks under your own name.
3. Connect the repo as a Git folder. The steps are in the [README](README.md#setup).

## Git flow

1. **Pull first.** Pull `main` before you start any work.
2. **Branch.** Make a new branch named for the work:
   - `feature/raw-dpwh-projects` for new work
   - `fix/clean-dates` for a fix
   - `docs/source-cards` for docs
   - If the name is taken, add your name, like `feature/raw-dpwh-projects-bri`.
3. **Commit small.** One change per commit, with a message that says what changed, like `Add raw load for DPWH projects`.
4. **Open a pull request** into `main`. Fill in the template and link the issue with `Closes #12`.
5. **Review.** One teammate reads it and approves. Then Kinah merges.
6. **Pull again** after a merge, so you have the latest `main`.

Never push straight to `main`. Everyone commits from their own account, so the history shows who did what.

## Names

Use the same names in code, docs and diagrams.

| Thing | Pattern | Example |
| --- | --- | --- |
| Notebook | `NN_layer_source` | `01_raw_dpwh_projects` |
| Schema | the layer name | `raw`, `clean`, `mart`, `validation` |
| Table | what it holds, in snake_case | `clean.projects` |
| Column | snake_case, no spaces | `contract_id`, `amount_paid` |

## Data quality

Every table gets checks. Save the results in `validation.dq_results` with these columns:

| column | data_quality_check | failed_rows | total_rows | percentage | status |
| --- | --- | --- | --- | --- | --- |
| contract_id | not null | 0 | 1000 | 0.00 | PASS |

If a critical check fails, the run stops. Do not skip a failed check to make the run pass.

## Keep it safe

- Never commit keys, tokens or passwords, even inside a notebook cell.
- Do not commit data files. Data lives in Databricks tables and volumes.
- Only use sources that are public and listed in the README.

## Keep it clean

- Put test work in a branch, not in `main`.
- When you rename or move a file, fix every link that points to it.
- Delete or clearly label old files, so no one runs the wrong one.

## Found a problem?

Open an issue with the **Data bug** template. Say what you ran, what you expected and what you got.
