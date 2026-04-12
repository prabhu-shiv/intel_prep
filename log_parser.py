import sys
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Log file analyzer")
    parser.add_argument("--file", required=True, help="Path to log file")
    return parser.parse_args()

def parse_log(filename):
    errors = []
    warnings = []

    try:
        with open(filename, "r") as f:
            lines = f.readlines()
    except FileNotFoundError as e:
        print(f"Error opening file {filename}: {e}")
        sys.exit(1)

    for line in lines:
        if "ERROR" in line:
            errors.append(line.strip())
        elif "WARNING" in line:
            warnings.append(line.strip())

    return errors, warnings


def print_report(filename, errors, warnings):
    print("=" * 50)
    print(f"LOG ANALYSIS REPORT - {filename}")
    print("=" * 50)
    print(f"Total errors found: {len(errors)}")
    print(f"Total warnings found: {len(warnings)}")
    print()

    if errors:
        print("ERRORS:")
        for i, error in enumerate(errors, start=1):
            print(f"[{i}] {error}")
        print()

    if warnings:
        print("WARNINGS:")
        for i, warning in enumerate(warnings, start=1):
            print(f"[{i}] {warning}")
        print()

    print("=" * 50)

def main():
    args = parse_args()
    errors, warnings = parse_log(args.file)
    print_report(args.file, errors, warnings)

if __name__ == "__main__":
    main()