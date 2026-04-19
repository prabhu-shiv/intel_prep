# Intel Prep Tools

This repository contains two small Python command-line utilities:

1. A log analyzer that scans `.log` files for `ERROR` and `WARNING` entries.
2. A system checker that runs basic environment and hardware-related checks.

## Project contents

- `log_parser.py` - parses log files and writes a summary report.
- `system_check.py` - runs system health and environment checks.
- `test_parser.py` - tests for log parser behavior.
- `test_system_check.py` - tests for system check helpers.
- `logs/` - sample log files (`system.log`, `gpu.log`, `network.log`).

## Requirements

- Python 3.8+
- `pytest` for running tests

Install test dependency:

```bash
python3 -m pip install pytest
```

## Log analyzer

### What it does

`log_parser.py`:
- Accepts a log directory with `--dir`.
- Finds files ending in `.log`.
- Extracts lines containing uppercase `ERROR` and `WARNING`.
- Writes a structured summary to `report.txt`.

### Run it

```bash
python3 log_parser.py --dir logs
```

## System checker

### What it does

`system_check.py` runs these checks and reports pass/fail:
- Python version (`python3 --version`)
- Disk space command output (`df -h /`)
- Disk usage threshold (`df /`, fails if usage is above 90%)
- Memory info (`free -h`)
- OS info (`uname -a`)
- Git version (`git --version`)

Each check logs details and returns a boolean result. The script exits with status code `1` if any check fails.

### Run it

```bash
python3 system_check.py
```

## Tests

Run all tests:

```bash
pytest -q
```

Current test coverage includes:
- log parsing behavior
- log file filtering
- `run_command()` handling for a nonexistent command
