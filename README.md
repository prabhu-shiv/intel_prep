# Intel Prep Tools

This repository contains a set of small Python command-line utilities:

1. A log analyzer that scans `.log` files for `ERROR` and `WARNING` entries.
2. A system checker that runs basic environment and hardware-related checks.
3. Hardware utilization monitoring

## Project contents

- `log_parser.py` - parses log files and writes a summary report.
- `system_check.py` - runs system health and environment checks.
- `test_parser.py` - tests for log parser behavior.
- `test_system_check.py` - tests for system check helpers.
- `logs/` - sample log files (`system.log`, `gpu.log`, `network.log`).
- `hw_monitor.py` - monitors CPU utilization under workload and generates a plot

## Requirements

- Python 3.8+
- `pytest` for running tests

Install test dependency:

```bash
python3 -m pip install pytest
```
```bash
python3 -m pip install pytest psutil matplotlib
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

## Hardware monitor

### What it does

`hw_monitor.py` performs real-time CPU monitoring under synthetic workload:
- Detects: CPU model `lscpu`, GPU model `lspci`, NPU
- Generates CPU load using multiprocessing
- Samples CPU utilization using `psutil`
- Computes: Average usage, Peak usage, Minimum usage
- Plots utilization graph `utilization.png`

The workload runs in parallel across all CPU cores.

### Run it

```bash
python3 hw_monitor.py --duration 10
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
- hardware monitoing
