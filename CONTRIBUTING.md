# How we work

These rules help five people build one pipeline without breaking each other's work.

## Before you start

1. Send Kinah your GitHub username so she can add you to the repo.
2. In Databricks, open **Settings**, then **Linked accounts**, and link your GitHub account. This lets you commit from Databricks under your own name.
3. Connect the repo as a Git folder. The steps are in the [README](README.md#setup).

## Git flow

1. **Pull first.** Pull `main` before you start any work.
2. **Branch.** Make a new branch named for the work:
   - `feature/bronze-dpwh-projects` for new work
   - `fix/silver-dates` for a fix
   - `docs/source-cards` for docs
   - If the name is taken, add your name, like `feature/bronze-dpwh-projects-bri`.
3. **Commit small.** One change per commit, with a message that says what changed, like `Add bronze load for DPWH projects`.
4. **Open a pull request** into `main`. Fill in the template and link the issue with `Closes #12`.
5. **Review.** One teammate reads it and approves. Then Kinah merges.
6. **Pull again** after a merge, so you have the latest `main`.

Never push straight to `main`. Everyone commits from their own account, so the history shows who did what.

## Names

Use the same names in code, docs and diagrams.

| Thing | Pattern | Example |
| --- | --- | --- |
| Notebook | `NN_layer_source` | `01_bronze_dpwh_projects` |
| Schema | the layer name | `bronze`, `silver`, `gold`, `validation` |
| Table | what it holds, in snake_case | `silver.projects` |
| Column | snake_case, no spaces | `contract_id`, `amount_paid` |

## Data quality

Every table gets checks. Save the results in `validation.dq_results` with these columns:

| column | data_quality_check | failed_rows | total_rows | percentage | status |
| --- | --- | --- | --- | --- | --- |
| contract_id | not null | 0 | 1000 | 0.00 | PASS |

If a critical check fails, the run stops. Do not skip a failed check to make the run pass.

## Using AI tools

AI can help us build faster, but we own everything we ship. These rules come from our capstone kickoff with FTW.

**The four gates.** Ask these before you use AI on project work. If any answer is no, stop.

| Gate | Ask yourself |
| --- | --- |
| 1. Data | Am I allowed to share this? |
| 2. AI | Is this tool the right place for it? |
| 3. Output | Can I check what the AI made? |
| 4. Accountability | Can I explain and defend the result? |

**What we give AI.**

| Color | What | Rule |
| --- | --- | --- |
| Green | Explaining Spark, debugging, boilerplate code and tests, docs, SQL ideas, brainstorming | Fine to use. Still review the output. |
| Yellow | Cleaning rules, schema changes, transformation logic, reading results | AI can suggest. A person decides and writes down why. |
| Red | Keys, tokens and passwords, private data, compliance calls, direct changes to the final workspace, decisions about people | Never. |

**Share the least you can.** Give AI the schema, a few fake rows, the error message and the code. Never whole tables or keys.

**Check before you merge.** Before AI-helped code goes into `main`, ask: Does it work? Does it scale? Is it safe? Can we rerun it and trace every number? Can I defend it? The pull request form has these questions.

**Checks live in code.** If AI suggests a data quality check, turn it into a real check in `validation.dq_results`. Do not just trust a chat that says the data looks fine.

## Keep it safe

- Never commit keys, tokens or passwords, even inside a notebook cell.
- Do not commit data files. Data lives in Databricks tables and volumes.
- Only use sources that are public and listed in the README.

## Keep it clean

- Put test work in a branch, not in `main`.
- When you rename or move a file, fix every link that points to it.
- Delete or clearly label old files, so no one runs the wrong one.

## Where we talk

- **Messenger:** day-to-day team chat
- **Slack:** the official FTW channel, for pins and context
- **Viber:** our chat with our SI and mentor

If we decide something in chat, write it in the team doc too.

## Found a problem?

Open an issue with the **Data bug** template. Say what you ran, what you expected and what you got.
