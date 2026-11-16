# Python coding conventions

Conventions for Python script projects. See `references/setup.md` in this skill for the Python values and the script template, and the `scripting` skill for the rules every command-line script follows.

## Quick Reference: Required Standards for Scripts

When creating or modifying a Python script, ensure ALL of the following are met:

- Arguments: `argparse`.
- Logging: the `logging` module, with `setup_logging(log_level, log_file)`.
- Progress: `tqdm`.
- Errors: `sys.exit(code)`.
- Documentation: type hints and Google-style docstrings on every function.
- Libraries: `import` statements in groups.
- Main: `if __name__ == "__main__":`.

## Command-line Arguments

Use the `argparse` module. Follow "Command-line flags" in the `scripting` skill, and these Python details:

1. Use `ArgumentParser` with a `description` and an `epilog`.
2. Set `type` (for example `type=Path`, `type=int`) and `metavar` on every argument.
3. Give every optional argument a `default`, and use `required=True` only for required arguments.
4. Use `action="store_true"` for an on/off flag.
5. Use `choices` when an argument has a limited set of valid values.
6. Group related arguments with `add_argument_group()` for a complex command-line interface.
7. The default for `--log-file` is `Path("logs") / f"{Path(__file__).stem}.log"`.
8. `argparse` exits with status 2 by itself when the arguments are invalid, so it needs no extra code.

See `parse_arguments()` in the script template in `references/setup.md`.

## Logging Configuration

Use the `logging` module. Follow "Logging" in the `scripting` skill, and these Python details:

1. Log with `logger = logging.getLogger(__name__)` at module level, and call `logger.info()`, `logger.warning()`, and `logger.error()`.
2. Open the file handler with `mode="w"`, so that each run starts a new log file.
3. Create the log folder with `log_file.parent.mkdir(parents=True, exist_ok=True)`.
4. Set the line format with `format` and `datefmt` in `logging.basicConfig()`.

See `setup_logging()` in the script template in `references/setup.md`.

## Progress bars

Use the `tqdm` package.

1. Wrap the thing you loop over: `for item in tqdm(items, desc="Processing"):`.
2. For a loop where the number of steps is not the length of a list, use `with tqdm(total=n, desc="Processing") as bar:` and call `bar.update(1)` once per step.

See `process_records()` in the script template in `references/setup.md`.

## Error Handling and Exit Codes

Follow "Exit codes" in the `scripting` skill, and these Python details:

1. Set the exit code with `sys.exit(code)`, never with bare `exit()` or `raise SystemExit`.
2. Wrap the main logic in `try`/`except` and catch specific exceptions:
   - `FileNotFoundError`, `PermissionError` -> log the error, exit with code 3
   - `ValueError`, `TypeError` -> log the error, exit with code 4
   - `Exception` -> log the error with its traceback (`logger.exception()`), exit with code 1

See `main()` in the script template in `references/setup.md`.

## Function Documentation

Follow "Documentation" in the `scripting` skill, and these Python details:

1. Document every function with a Google-style docstring: a one-line summary, then optional "Args:", "Returns:", and "Raises:" sections.
2. Use type hints for all parameters and return values. Use `Optional[Type]` from `typing` for a parameter that can be None.

See any function in the script template in `references/setup.md`.

## Library Loading

Import libraries in this order, with the imports of each group in alphabetical order:

1. Standard library imports.
2. Third-party imports.
3. Local imports.

See "Import packages" in the script template in `references/setup.md`.

## Python Code Style

1. Use snake_case for function and variable names, UPPER_CASE for constants, and PascalCase for classes.
2. Use four spaces for indentation.
3. Use `Path` from `pathlib` for file and folder paths, not `str`.

## Plotting

Follow "Plotting" in the `scripting` skill. Draw plots with `seaborn`, not with `matplotlib` directly, and add `seaborn` to the environment yml. Details:

1. Call `sns.set_theme(style="whitegrid")` once, before the first plot.
2. Pass `palette=sns.color_palette("viridis", n_colors=n)` for categorical colors, where `n` is the number of categories.
3. `seaborn` has no setting for a thousands separator, so format the axis with `StrMethodFormatter` from `matplotlib.ticker`. This is the only use of `matplotlib` in the script.

Example:

```python
import seaborn as sns
from matplotlib.ticker import StrMethodFormatter

sns.set_theme(style="whitegrid")
n_groups = df["group"].nunique()
ax = sns.barplot(
    data=df, x="sample", y="reads", hue="group",
    palette=sns.color_palette("viridis", n_colors=n_groups)
)
ax.yaxis.set_major_formatter(StrMethodFormatter("{x:,.0f}"))
ax.figure.tight_layout()
ax.figure.savefig(output_dir / "reads_by_sample.png")
```

## Data handling

Follow "Data handling" in the `scripting` skill, with these `pandas` details. Add `pandas` to the environment yml.

1. Name the identifier columns as text with `dtype`: `pd.read_csv(path, dtype={"sample": str})`. This keeps leading zeros. `pandas` keeps the column names as they are in the file.
2. `pandas` reads the text NA as a missing value, even in a column read as text. When an identifier can be the text NA, also pass `keep_default_na=False`, and name the missing-value strings with `na_values`.
