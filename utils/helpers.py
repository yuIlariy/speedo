import os
import json
import subprocess
import random
import platform
import psutil
import matplotlib.pyplot as plt

from datetime import datetime
from config import RESULTS_LOG, TREND_IMAGE


def get_sysinfo() -> str:
    sys = platform.uname()
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage("/")
    boot = datetime.fromtimestamp(psutil.boot_time())
    now = datetime.utcnow()
    delta = now - boot

    weeks, days = divmod(delta.days, 7)
    hours, rem_secs = divmod(delta.seconds, 3600)
    minutes = rem_secs // 60

    formatted_uptime = []
    if weeks: formatted_uptime.append(f"{weeks}w")
    if days: formatted_uptime.append(f"{days}d")
    if hours: formatted_uptime.append(f"{hours}h")
    if minutes: formatted_uptime.append(f"{minutes}m")
    uptime_str = " ".join(formatted_uptime)

    # ✅ Grab CPU name via shell for clarity
    try:
        cpu_name = subprocess.check_output(
            "lscpu | grep 'Model name' | awk -F: '{print $2}'",
            shell=True
        ).decode().strip()
    except Exception:
        cpu_name = sys.processor or "Unknown"

    return (
        f"<b>🖥️ System</b>: {sys.system} {sys.release} ({sys.machine})\n"
        f"<b>🧮 CPU</b>: {cpu_name}\n"
        f"<b>⏱️ Uptime</b>: {uptime_str}\n"
        f"<b>💾 Memory</b>: {mem.used // (1024 ** 3)}GB / {mem.total // (1024 ** 3)}GB\n"
        f"<b>📀 Disk</b>: {disk.used // (1024 ** 3)}GB / {disk.total // (1024 ** 3)}GB\n"
        f"<b>⚙️ CPU Usage</b>: {psutil.cpu_percent()}%"
    )



def get_uptime() -> str:
    boot_time = datetime.fromtimestamp(psutil.boot_time())
    now = datetime.utcnow()
    return str(now - boot_time).split('.')[0]


def mask_ip(ip: str) -> str:
    segments = ip.split(".")
    masked_segments = []
    for seg in segments:
        masked = ""
        for ch in seg:
            if ch.isdigit() and random.random() < 0.5:
                masked += random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
            else:
                masked += ch
        masked_segments.append(masked)
    return ".".join(masked_segments)


def save_result(download, upload, ping, timestamp):
    os.makedirs("results", exist_ok=True)
    data = {
        "timestamp": timestamp,
        "download": round(download, 2),
        "upload": round(upload, 2),
        "ping": round(ping, 2)
    }
    existing = []
    if os.path.exists(RESULTS_LOG):
        with open(RESULTS_LOG) as f:
            existing = json.load(f)
    existing.append(data)
    with open(RESULTS_LOG, "w") as f:
        json.dump(existing[-30:], f, indent=2)


def generate_plot():
    if not os.path.exists(RESULTS_LOG):
        return None
    with open(RESULTS_LOG) as f:
        data = json.load(f)

    timestamps = [datetime.fromisoformat(d["timestamp"]) for d in data]
    downloads = [d["download"] for d in data]
    uploads = [d["upload"] for d in data]

    plt.figure(figsize=(10, 5))
    plt.plot(timestamps, downloads, label="Download (Mbps)", color="blue")
    plt.plot(timestamps, uploads, label="Upload (Mbps)", color="green")
    plt.legend()
    plt.title("Speed Trends")
    plt.xlabel("Time")
    plt.ylabel("Mbps")
    plt.grid()
    plt.tight_layout()
    plt.savefig(TREND_IMAGE)

    return TREND_IMAGE


