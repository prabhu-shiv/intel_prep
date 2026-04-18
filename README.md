# Intel Prep Log Analyzer

A small Python CLI tool that scans `.log` files in a directory and generates a consolidated error/warning report.

## What this project does

`log_parser.py`:
- Accepts a log directory with `--dir`.
- Finds files ending in `.log` in that directory.
- Extracts lines containing `ERROR` and `WARNING`.
- Writes a structured summary to `report.txt`.

## Repository layout

- `log_parser.py` – main parser/report generator.
- `logs/` – sample input log files (`system.log`, `gpu.log`, `network.log`).

## Requirements

- Python 3.8+
- No third-party dependencies

## Usage

From the repository root:

```bash
python3 log_parser.py --dir logs
```

This command regenerates `report.txt` based on all `.log` files in `logs/`.

## Example output

The generated `report.txt` contains one section per log file with:
- total errors
- total warnings
- numbered list of error lines
- numbered list of warning lines

## Notes and behavior

- The parser currently detects only uppercase tokens: `ERROR` and `WARNING`.
- If the provided directory does not exist, the script exits with an error.
- If a log file cannot be opened, the script exits immediately.
- Output file path is fixed to `report.txt` in the current working directory.

## Quick development ideas

Potential improvements:
- Support case-insensitive matching (`error`, `warning`).
- Add output path as a CLI option (e.g., `--out report.txt`).
- Include `INFO` counts or severity filters.
- Add unit tests for parsing and reporting functions.
