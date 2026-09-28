# Style guide

Short rules for how we write and code. They come from the guides listed at the end.

## Write so anyone can follow

1. **One idea per sentence.** If a sentence needs a semicolon or a dash, split it in two.
2. **Say the main thing first.** Put what the reader needs most in the first line.
3. **Talk to the reader.** Use "you" and "we". Say who does what: "The notebook loads the table", not "The table is loaded".
4. **Use present tense.** Write "loads", not "will load".
5. **Use short, common words.** Say "start", not "commence". Explain a new term in one line the first time you use it.
6. **Number the steps.** Put one action in each step. Then say what the reader should see.
7. **Put the condition first.** Write "If the check fails, stop the run", not the other way around.
8. **Write headings in sentence case.** Start a task heading with a verb, like "Run the pipeline".
9. **Make links say where they go.** Never write "click here".
10. **Put code in code font.** File names, tables, columns and commands go in backticks, like `silver.projects`.
11. **Use tables for real data only.** Fill every cell. Write "None" if there's nothing.
12. **Keep each fact in one place.** Link to it instead of copying it.
13. **Update the docs in the same pull request as the code.**

Our house rules: no em dashes, no semicolons, and a 7th grade reading level or lower. To check the grade, paste your text into a free readability checker like [WebFX Read-Able](https://www.webfx.com/tools/read-able/).

## Write short, clear code

1. **Keep names and links in `buildabida/config.py`.** Notebooks import them. Never copy a table name or a link into a notebook.
2. **Put helpers in the `buildabida` folder, not in notebooks.** Import them with `from buildabida import api, config`. Don't use `%run`.
3. **Give each step its own cell.** Only print or display what you need to check.
4. **Name columns in snake_case.** True or false columns start with `is_` or `has_`. DataFrame names end in `_df`.
5. **Build columns in one `select`.** Rename with `.alias()` instead of long `withColumn` chains.
6. **Keep chains short.** Wrap a chain of up to 5 steps in parentheses. Never end a line with a backslash.
7. **Always say how to join.** Write `how="left"` or `how="inner"`. Don't use right joins.
8. **Use built-in Spark functions.** Avoid Python UDFs. They're slower and harder to check.
9. **Name your numbers.** Put a number like a date cutoff in a named constant, with a comment that says why.
10. **Catch the error you expect.** Write `except requests.RequestException`, not `except Exception`.
11. **Write data quality rules as data.** Keep the rules in a list, and run them all in one place.

Here's a short, clear `select`:

```python
projects_df = raw_df.select(
    F.col("contractId").alias("contract_id"),
    F.col("budget").cast("decimal(18,2)").alias("budget"),
    F.to_date("startDate").alias("start_date"),
)
```

## Checks that run for you

Every pull request runs these checks. A red X means a check found a problem. Click **Details** to see where.

| Check | What it looks at | How to fix it |
| --- | --- | --- |
| Ruff | Python code | Fix the line it names. |
| Links | Links in Markdown files | Fix the path, or add the missing file. |
| Markdown | The layout of Markdown files | Fix the line it names. |
| Writing tips | Semicolons, dashes, long sentences and wordy phrases | Split or trim the sentence. These are tips, so they never block a merge. |

## Where these rules come from

- [Google developer documentation style guide](https://developers.google.com/style)
- [Microsoft Writing Style Guide](https://learn.microsoft.com/en-us/style-guide/welcome/)
- [Diátaxis](https://diataxis.fr/), for how we split our docs
- [Plain language guide](https://digital.gov/guides/plain-language/)
- [Write the Docs guide](https://www.writethedocs.org/guide/)
- [Palantir PySpark style guide](https://github.com/palantir/pyspark-style-guide)
- [Databricks notebook best practices](https://docs.databricks.com/aws/en/notebooks/best-practices)
- [Ruff](https://docs.astral.sh/ruff/)
