import sys
import argparse
import os

def parse_args():
    parser = argparse.ArgumentParser(description="Log file analyzer")
    parser.add_argument("--dir", required=True, help="Path to directory containing log files")
    return parser.parse_args()

def get_log_files(directory):
    log_files = []
    for file in os.listdir(directory):
        if file.endswith('.log'):
            log_files.append(os.path.join(directory, file))
    return log_files

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


def print_report(filename, errors, warnings, f):
    f.write("=" * 50 + "\n")
    f.write(f"LOG ANALYSIS REPORT - {filename}\n")
    f.write("=" * 50 + "\n")
    f.write(f"Total errors found: {len(errors)}\n")
    f.write(f"Total warnings found: {len(warnings)}\n")
    f.write("\n")

    if errors:
        f.write("ERRORS:\n")
        for i, error in enumerate(errors, start=1):
            f.write(f"[{i}] {error}\n")
        f.write("\n")

    if warnings:
        f.write("WARNINGS:\n")
        for i, warning in enumerate(warnings, start=1):
            f.write(f"[{i}] {warning}\n")
        f.write("\n")

    f.write("=" * 50 + "\n")

def main():
    args = parse_args()
    if not os.path.isdir(args.dir):
        print(f"Error: Directory '{args.dir}' does not exist")
        sys.exit(1)
    log_files = get_log_files(args.dir)
    with open("report.txt", "w") as f:
        for log_file in log_files:
            errors, warnings = parse_log(log_file)
            print_report(log_file, errors, warnings, f)

if __name__ == "__main__":
    main()