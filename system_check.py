import subprocess
import logging
import sys


def setup_logging():
    logging.basicConfig(
        format="%(levelname)s: %(message)s",
        level=logging.INFO
    )


def run_command(command):
    try:
        result = subprocess.run(command, capture_output=True, text=True)
    except FileNotFoundError:
        logging.error(f"Command not found: {' '.join(command)}")
        return None
    if result.returncode != 0:
        logging.error(f"Command failed: {' '.join(command)}")
        logging.error(f"stderr: {result.stderr.strip()}")
        return None
    return result.stdout.strip()


def check_python_version():
    output = run_command(["python3", "--version"])
    if output is None:
        return False
    logging.info(f"Python version: {output}")
    if "3." in output:
        logging.info("PASS: Python 3.x detected")
        return True
    logging.error("FAIL: Python 3.x not found")
    return False


def check_disk_space():
    output = run_command(["df", "-h", "/"])
    if output is None:
        return False
    lines = output.split("\n")
    logging.info("Disk space output:")
    logging.info(lines[0])
    if len(lines) > 1:
        logging.info(lines[1])
    return True


def check_memory():
    output = run_command(["free", "-h"])
    if output is None:
        return False
    logging.info("Memory output:")
    for line in output.split("\n"):
        logging.info(line)
    return True


def check_os_info():
    output = run_command(["uname", "-a"])
    if output is None:
        return False
    logging.info("OS info:")
    for line in output.split("\n"):
        logging.info(line)
    return True


def check_git_version():
    output = run_command(["git", "--version"])
    if output is None:
        return False
    logging.info("Git version:")
    logging.info(output)
    return True


def main():
    setup_logging()
    results = []
    results.append(check_python_version())
    results.append(check_disk_space())
    results.append(check_memory())
    results.append(check_os_info())
    results.append(check_git_version())

    passed = sum(results)
    total = len(results)
    print(f"\n{'='*40}")
    print(f"Results: {passed}/{total} checks passed")
    print(f"{'='*40}")
    if passed != total:
        sys.exit(1)


if __name__ == "__main__":
    main()
