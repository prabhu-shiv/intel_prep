import psutil
import subprocess
import time
import logging
import argparse
import matplotlib.pyplot as plt
import multiprocessing


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


def _worker(duration):
    end_time = time.time() + duration
    result = 0
    while time.time() < end_time:
        for i in range(10**5):
            result += i * i


def run_workload(duration):
    logging.info("Running CPU workload...")
    time.sleep(2)  # Give monitor a moment to start
    cores = multiprocessing.cpu_count()
    processes = []
    for _ in range(cores):
        p = multiprocessing.Process(target=_worker, args=(duration,))
        p.start()
        processes.append(p)
    for p in processes:
        p.join()
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
    workload_thread = threading.Thread(target=run_workload, args=(args.duration,))

    workload_thread.start()

    cpu_samples = monitor_cpu(args.duration)
    print(f"Collected {len(cpu_samples)} samples")
    print(f"\nSummary:")
    print(f"  Average CPU usage: {sum(cpu_samples)/len(cpu_samples):.1f}%")
    print(f"  Peak CPU usage: {max(cpu_samples):.1f}%")
    print(f"  Min CPU usage: {min(cpu_samples):.1f}%")

    workload_thread.join()

    plot_utilization(cpu_samples, args.duration)


if __name__ == "__main__":
    main()
