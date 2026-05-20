import argparse
import logging
import threading
import time
import psutil
import numpy as np
import onnxruntime as ort
import matplotlib.pyplot as plt

logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)

# ── Agent base ────────────────────────────────────────────────
class InferenceAgent:
    def __init__(self, device, model_path):
        self.device = device
        self.model_path = model_path
        self.available = False
        self.session = None
        self.utilization = []
        self.running = False

    def setup(self):
        raise NotImplementedError

    def run_inference(self, duration):
        raise NotImplementedError

    def monitor(self, duration, interval=1):
        raise NotImplementedError


# ── CPU Agent ─────────────────────────────────────────────────
class CPUAgent(InferenceAgent):
    def __init__(self, model_path):
        super().__init__("CPU", model_path)

    def setup(self):
        try:
            self.session = ort.InferenceSession(
                self.model_path, providers=["CPUExecutionProvider"]
            )
            self.available = True
            logging.info("CPU agent ready")
        except Exception as e:
            logging.error(f"CPU agent setup failed: {e}")

    def run_inference(self, duration):
        if not self.available:
            return
        input_name = self.session.get_inputs()[0].name
        end_time = time.time() + duration
        count = 0
        while time.time() < end_time:
            dummy = np.random.randn(1, 3, 224, 224).astype(np.float32)
            self.session.run(None, {input_name: dummy})
            count += 1
        logging.info(f"CPU: completed {count} inference runs")

    def monitor(self, duration, interval=1):
        samples = []
        for _ in range(int(duration / interval)):
            samples.append(psutil.cpu_percent(interval=interval))
        self.utilization = samples


# ── GPU Agent ─────────────────────────────────────────────────
class GPUAgent(InferenceAgent):
    def __init__(self, model_path):
        super().__init__("GPU", model_path)
        self.provider_used = None

    def setup(self):
        available = ort.get_available_providers()
        
        # Priority order — pick first available GPU provider
        gpu_providers = [
            "CUDAExecutionProvider",       # NVIDIA
            "ROCMExecutionProvider",       # AMD
            "DmlExecutionProvider",        # Windows DirectML (any GPU)
            "OpenVINOExecutionProvider",   # Intel
            "CoreMLExecutionProvider",     # Apple
        ]

        for provider in gpu_providers:
            if provider in available:
                try:
                    self.session = ort.InferenceSession(
                        self.model_path, providers=[provider]
                    )
                    self.provider_used = provider
                    self.available = True
                    logging.info(f"GPU agent ready — using {provider}")
                    return
                except Exception as e:
                    logging.warning(f"GPU agent: {provider} failed: {e}")

        logging.warning("GPU agent: no GPU execution provider available")

    def run_inference(self, duration):
        if not self.available:
            logging.warning("GPU agent skipped — not available")
            return
        input_name = self.session.get_inputs()[0].name
        end_time = time.time() + duration
        count = 0
        while time.time() < end_time:
            dummy = np.random.randn(1, 3, 224, 224).astype(np.float32)
            self.session.run(None, {input_name: dummy})
            count += 1
        logging.info(f"GPU: completed {count} inference runs")

    def monitor(self, duration, interval=1):
        if not self.available:
            self.utilization = []
            return
        # GPU monitoring placeholder — extend with ROCm/CUDA tools
        self.utilization = [0] * int(duration / interval)


# ── NPU Agent ─────────────────────────────────────────────────
class NPUAgent(InferenceAgent):
    def __init__(self, model_path):
        super().__init__("NPU", model_path)
        self.provider_used = None

    def setup(self):
        available = ort.get_available_providers()

        npu_providers = [
            "OpenVINOExecutionProvider",  # Intel NPU
            "QNNExecutionProvider",       # Qualcomm NPU
            "CoreMLExecutionProvider",    # Apple Neural Engine
        ]

        for provider in npu_providers:
            if provider in available:
                try:
                    self.session = ort.InferenceSession(
                        self.model_path, providers=[provider]
                    )
                    self.provider_used = provider
                    self.available = True
                    logging.info(f"NPU agent ready — using {provider}")
                    return
                except Exception as e:
                    logging.warning(f"NPU agent: {provider} failed: {e}")

        logging.warning("NPU agent: no NPU detected on this hardware — skipping")

    def run_inference(self, duration):
        if not self.available:
            return  # silently skip — warning already logged in setup()
        input_name = self.session.get_inputs()[0].name
        end_time = time.time() + duration
        count = 0
        while time.time() < end_time:
            dummy = np.random.randn(1, 3, 224, 224).astype(np.float32)
            self.session.run(None, {input_name: dummy})
            count += 1
        logging.info(f"NPU: completed {count} inference runs")

    def monitor(self, duration, interval=1):
        if not self.available:
            self.utilization = []
            return
        # NPU utilization monitoring — extend per platform
        self.utilization = [0] * int(duration / interval)


# ── Orchestrator ──────────────────────────────────────────────
def run_agent(agent, duration):
    inference_thread = threading.Thread(target=agent.run_inference, args=(duration,))
    monitor_thread = threading.Thread(target=agent.monitor, args=(duration,))
    inference_thread.start()
    monitor_thread.start()
    inference_thread.join()
    monitor_thread.join()


# ── Plot ──────────────────────────────────────────────────────
def plot_results(agents):
    plt.figure(figsize=(12, 5))
    for agent in agents:
        if agent.utilization:
            timestamps = list(range(len(agent.utilization)))
            plt.plot(timestamps, agent.utilization, label=f"{agent.device} %")
    plt.xlabel("Time (seconds)")
    plt.ylabel("Utilization %")
    plt.title("Device Utilization During Inference")
    plt.ylim(0, 100)
    handles, labels = plt.gca().get_legend_handles_labels()
    if handles:
        plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("inference_utilization.png")
    logging.info("Plot saved to inference_utilization.png")
    plt.show()


# ── CLI ───────────────────────────────────────────────────────
def parse_args():
    parser = argparse.ArgumentParser(description="Inference agent — CPU/GPU/NPU")
    parser.add_argument(
        "--device",
        choices=["cpu", "gpu", "npu", "all"],
        default="cpu",
        help="Device to run inference on"
    )
    parser.add_argument("--duration", type=int, default=10, help="Duration in seconds")
    parser.add_argument("--model", default="mobilenetv2.onnx", help="Path to ONNX model")
    return parser.parse_args()


def main():
    args = parse_args()

    device_map = {
        "cpu": [CPUAgent],
        "gpu": [GPUAgent],
        "npu": [NPUAgent],
        "all": [CPUAgent, GPUAgent, NPUAgent]
    }

    agents = [cls(args.model) for cls in device_map[args.device]]

    for agent in agents:
        agent.setup()

    threads = []
    for agent in agents:
        t = threading.Thread(target=run_agent, args=(agent, args.duration))
        threads.append(t)

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    plot_results(agents)

    print(f"\n{'='*40}")
    for agent in agents:
        if agent.utilization:
            print(f"{agent.device} — avg: {sum(agent.utilization)/len(agent.utilization):.1f}%  peak: {max(agent.utilization):.1f}%")
        else:
            print(f"{agent.device} — not available")
    print(f"{'='*40}")


if __name__ == "__main__":
    main()