import psutil, socket, platform, matplotlib.pyplot as plt
from io import BytesIO
from datetime import datetime
import subprocess, shutil
import random

CAPTION_BANK = [
    "📡 Monitoring the machine gods — telemetry inbound.",
    "🦔 VPS status served fresh. Nothing escapes this dashboard.",
    "🔍 Full system scan complete. Operational excellence achieved.",
    "🚀 Telemetry check: speeds, cores, and cosmic load curves.",
    "🧊 Cool, quiet, stable. Your VPS is meditating.",
    "📈 Performance snapshot: clean lines, zero regrets.",
    "🪄 Load balances, disks spin, packets fly. Magic confirmed.",
    "🎯 Speedtest fusion and system vitals — looking sharp.",
    "🧵 Telemetry weave complete. You’re plugged into the core.",
    "⚙️ Everything’s under control. Just how you built it.",
]

async def generate_syschart():
    cpu_usage = psutil.cpu_percent(interval=1)
    dark_mode = cpu_usage > 50

    plt.style.use('dark_background' if dark_mode else 'default')
    fig, axs = plt.subplots(2, 2, figsize=(10, 6))

    # ✨ Inject a random caption as chart title
    fig.suptitle(random.choice(CAPTION_BANK), fontsize=14)

    hostname = socket.gethostname()
    uptime = datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
    cpu_model = platform.processor()

    # RAM & Disk
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    axs[0,0].barh(['RAM', 'Disk'], [mem.percent, disk.percent], color=["deepskyblue", "mediumseagreen"])
    axs[0,0].set_xlim(0, 100)
    axs[0,0].set_title("Resource Usage (%)")

    # Load avg
    load1, load5, load15 = psutil.getloadavg()
    axs[0,1].plot([1,5,15], [load1, load5, load15], marker='o', color='gold')
    axs[0,1].set_xticks([1,5,15])
    axs[0,1].set_title("Load Average")

    # CPU + Temp
    axs[1,0].bar(['CPU'], [cpu_usage], color='tomato')
    axs[1,0].set_ylim(0, 100)
    axs[1,0].set_title(f"CPU Usage (%) • Temp: {get_cpu_temp()}")

    # Speedtest + Net I/O
    net = run_speedtest()
    net_io = psutil.net_io_counters()
    net_text = (
        f"Ping: {net['Ping']}\n"
        f"Down: {net['Download']}\n"
        f"Up: {net['Upload']}\n"
        f"TX: {round(net_io.bytes_sent/1e6, 1)} MB\n"
        f"RX: {round(net_io.bytes_recv/1e6, 1)} MB"
    )
    axs[1,1].text(0.05, 0.6, net_text, fontsize=10)
    axs[1,1].axis('off')
    axs[1,1].set_title("Network & Speedtest")

    # Footer
    fig.text(0.5, 0.01, f"{hostname} • Uptime: {uptime} • CPU: {cpu_model}", ha='center', fontsize=8)

    buf = BytesIO()
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig(buf, format='png', dpi=150)
    buf.seek(0)
    return buf


