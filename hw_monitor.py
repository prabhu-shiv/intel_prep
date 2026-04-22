import psutil
import subprocess
import time
import logging
import argparse
import matplotlib.pyplot as plt


logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)


def get_cpu_info():
    result = subprocess.run(["lscpu"], capture_output=True, text=True)
    for line in result.stdout.split("\n"):
        if "Model name" in line:
            return line.split(":")[1].strip()
    return "Unknown CPU"


def get_gpu_info():
    result = subprocess.run(["lspci"], capture_output=True, text=True)
    for line in result.stdout.split("\n"):
        if "VGA" in line or "Display" in line:
            return line.split(":")[-1].strip()
    return "No GPU detected"


def get_npu_info():
    # NPU detection — expand later for Intel platforms
    return "No NPU detected on this hardware"


def monitor_cpu(duration, interval=1):
    samples = []
    for _ in range(int(duration / interval)):
        usage = psutil.cpu_percent(interval=interval)
        samples.append(usage)
    return samples


def run_workload():
    # CPU workload — matrix multiplication
    logging.info("Running CPU workload...")
    result = 0
    for i in range(10**7):
        result += i * i
    logging.info("Workload complete")


def plot_utilization(cpu_samples, duration):
    timestamps = [i for i in range(len(cpu_samples))]
    plt.figure(figsize=(10, 5))
    plt.plot(timestamps, cpu_samples, label="CPU %", color="blue")
    plt.xlabel("Time (seconds)")
    plt.ylabel("Utilization %")
    plt.title("Hardware Utilization During Workload")
    plt.ylim(0, 100)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("utilization.png")
    logging.info("Plot saved to utilization.png")
    plt.show()


def parse_args():
    parser = argparse.ArgumentParser(description="Hardware utilization monitor")
    parser.add_argument("--duration", type=int, default=10, help="Monitoring duration in seconds")
    return parser.parse_args()


def main():
    args = parse_args()

    logging.info(f"CPU: {get_cpu_info()}")
    logging.info(f"GPU: {get_gpu_info()}")
    logging.info(f"NPU: {get_npu_info()}")

    import threading
    workload_thread = threading.Thread(target=run_workload)
    workload_thread.start()

    cpu_samples = monitor_cpu(args.duration)
    workload_thread.join()

    plot_utilization(cpu_samples, args.duration)


if __name__ == "__main__":
    main()
    