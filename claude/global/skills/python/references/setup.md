# Python project setup

This file holds what is specific to Python script projects (not package or Jupyter notebook projects). The layout, naming, initialization steps, README content, and script structure that every script project shares are in the `scripting` skill. Read `references/coding.md` in this skill for the Python code rules.

## Python values

Use these values in the `scripting` setup:

- File extension: `.py`. Script names are snake_case.
- Primary tool: `python=3.14`. Extra packages: `tqdm`.
- `.gitignore` entries: the Python entries below.
- Run command: `python src/[project_name].py [arguments]`, in the project's environment (`mamba run -n [project-name] python src/[project_name].py`).
- Parse check: `mamba run -n [project-name] python -m py_compile src/[project_name].py`.

Make the script follow the Python sections of `references/coding.md`:

- `argparse` with `--log-level` and `--log-file` ("Command-line Arguments")
- logging with `setup_logging()` ("Logging Configuration")
- `tqdm` progress bars for loops over records or files ("Progress bars")
- error handling with the standard exit codes ("Error Handling and Exit Codes")
- type hints and Google-style docstrings on every function ("Function Documentation")
- imports in standard library, third-party, local order ("Library Loading")

When you validate, also run the parse check.

## File Templates

### config/[project-name].yml Template

This file specifies the conda environment for the project. Python-specific entries:

- Pin `python=3.14` when the yml is created.
- Include `tqdm`. Leave it unpinned until the environment resolves.
- Pin all other packages after the environment resolves (see "Environment yml" in the `project-setup` skill).

The `logging`, `argparse`, `pathlib`, and `typing` modules are part of the Python standard library, so they need no entry.

### src/[project_name].py Template Structure

This file is the main script for the project. It follows the section order in "Script structure" in the `scripting` skill, and the standards in `references/coding.md`:

```python
#!/usr/bin/env python
################################################################################
### [project_name].py
### [Contact block: see this client's CLAUDE.md]
### [Description]
################################################################################

################################################################################
### Import packages
################################################################################

# Standard library imports (alphabetical order within group)
import argparse
import logging
import sys
from pathlib import Path
from typing import Optional

# Third-party imports (alphabetical order within group)
from tqdm import tqdm
# Add other third-party imports here (e.g., pandas, numpy, etc.)

# Local imports (alphabetical order within group)
# Add local module imports here if any (e.g., from [project_name]_helper import ...)

# Note: Only import what is actually used. Remove unused imports.

################################################################################
### Constants
################################################################################

LOG_LEVELS = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

logger = logging.getLogger(__name__)

################################################################################
### Command-line arguments
################################################################################

def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments.

    argparse exits with status 2 when the arguments are invalid.

    Returns:
        Parsed arguments namespace.
    """
    parser = argparse.ArgumentParser(
        description="[Brief description of the utility]",
        epilog="For more information, see README.md",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    required = parser.add_argument_group("required arguments")
    required.add_argument(
        "--input-file",
        type=Path,
        required=True,
        metavar="FILE",
        help="Path to input file"
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("results"),
        metavar="DIR",
        help="Output directory (default: results)"
    )
    parser.add_argument(
        "--log-level",
        type=str,
        choices=LOG_LEVELS,
        default="INFO",
        metavar="LEVEL",
        help="Logging level: DEBUG, INFO, WARNING, ERROR, CRITICAL (default: INFO)"
    )
    parser.add_argument(
        "--log-file",
        type=Path,
        default=Path("logs") / f"{Path(__file__).stem}.log",
        metavar="FILE",
        help="Path to log file (default: logs/[project_name].log)"
    )
    return parser.parse_args()

################################################################################
### Logging configuration
################################################################################

def setup_logging(log_level: str = "INFO", log_file: Optional[Path] = None) -> None:
    """Configure logging for the script.

    Each run starts a new log file, so the log holds only the latest run.

    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Path to the log file, or None for logging to stderr only
    """
    handlers: list[logging.Handler] = []
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        handlers.append(logging.FileHandler(log_file, mode="w"))

    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=handlers if handlers else [logging.StreamHandler(sys.stderr)]
    )

################################################################################
### Processing functions
################################################################################

def process_records(records: list[str]) -> int:
    """Process a list of records, with a progress bar.

    Replace the body with the script's own work. Add more functions, in logical
    groups, each with type hints and a Google-style docstring.

    Args:
        records: The records to process

    Returns:
        The number of records processed
    """
    processed = 0
    for record in tqdm(records, desc="Processing records"):
        processed += 1
    logger.info(f"Processed {processed} records")
    return processed

################################################################################
### Main function
################################################################################

def main() -> None:
    """Run the script: parse arguments, set up logging, and process the input."""
    args = parse_arguments()
    setup_logging(args.log_level, args.log_file)

    try:
        if not args.input_file.exists():
            logger.error(f"Input file not found: {args.input_file}")
            sys.exit(3)
        logger.info("Processing started")
        records = args.input_file.read_text().splitlines()
        # Raise ValueError("what is wrong") for a problem in the input data.
        process_records(records)
        logger.info("Processing completed successfully")
    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        sys.exit(3)
    except PermissionError as e:
        logger.error(f"Permission denied: {e}")
        sys.exit(3)
    except (ValueError, TypeError) as e:
        logger.error(f"Invalid data: {e}")
        sys.exit(4)
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

The main script:

1. Starts with the shebang line `#!/usr/bin/env python`.
2. Calls `main()` only when it is run as a script (`__name__ == "__main__"`), so that importing the file loads the functions without running the analysis.
3. Imports its supporting modules, if it has any, from the same `src/` folder (for example `from [project_name]_helper import ...`).

### .gitignore Template

Append these entries to the template `.gitignore`:

```
# Python
__pycache__/
*.py[cod]
*$py.class
*.pyc
*.pyo
*.pyd
*.so
.Python
.env
.venv
```
