from io import BytesIO
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge
import psutil, socket, time, random
from datetime import datetime

# ─── Configurable Thresholds ─────────────────────────
ALERT = {
    "cpu": 85,
    "ram": 75,
    "disk": 80,
    "loadavg": 2.5
}

THEMES = {
    "dark":    {"bg": "#0e0e1c", "fg": "#ffffff"},
    "neon":    {"bg": "#000000", "fg": "#00ffff"},
    "minimal": {"bg": "#ffffff", "fg": "#333333"}
}

CAPTION_MOODS = {
    "dark":    "Dark ops 🕶️",
    "neon":    "Laser lanes 💡",
    "minimal": "Clean glide 🧼"
}

# ─── Gather System Metrics ───────────────────────────
def get_sys_metrics():
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage("/")
    net = psutil.net_io_counters()
    cpu = psutil.cpu_percent()
    load = psutil.getloadavg()

    return {
        "cpu": cpu,
        "ram": (mem.used / mem.total) * 100,
        "ram_text": f"{mem.used/1e9:.1f}/{mem.total/1e9:.1f} GB",
        "disk": disk.percent,
        "net_tx": f"{net.bytes_sent / 1e6:.1f}MB",
        "net_rx": f"{net.bytes_recv / 1e6:.1f}MB",
        "load": load,
        "hostname": socket.gethostname(),
        "uptime": int(time.time() - psutil.boot_time())
    }

# ─── Ring Style Helpers ──────────────────────────────
def draw_ring(ax, center, percent, label, alert=False, fg="#00bfff"):
    radius = 0.45
    theta = percent * 360 / 100
    ring = Wedge(center, radius, 0, theta, width=0.08, color=fg, alpha=0.8)
    ax.add_patch(ring)
    ax.text(*center, label, ha='center', va='center', fontsize=10,
            color="red" if alert else fg)

# ─── Render Image ────────────────────────────────────
def render_rings(theme="dark", metrics=None, caption_override=None):
    if not metrics:
        metrics = get_sys_metrics()

    style = THEMES.get(theme, THEMES["dark"])
    fig, ax = plt.subplots(figsize=(6,6))
    ax.set_facecolor(style["bg"])
    fig.patch.set_facecolor(style["bg"])
    ax.set_xlim(0, 2)
    ax.set_ylim(0, 2)
    ax.axis('off')

    # ─ Rings ─
    ring_specs = [
        ("cpu", (0.5,1.5), f"🧮 CPU {metrics['cpu']}%", metrics["cpu"] > ALERT["cpu"]),
        ("ram", (1.5,1.5), f"💾 RAM {metrics['ram']:.1f}%\n{metrics['ram_text']}", metrics["ram"] > ALERT["ram"]),
        ("disk", (0.5,0.5), f"📀 Disk {metrics['disk']}%", metrics["disk"] > ALERT["disk"]),
        ("net", (1.5,0.5), f"🌐 TX {metrics['net_tx']}\nRX {metrics['net_rx']}", False),
        ("load", (1,1), f"💡 Load {metrics['load'][0]:.1f}/{metrics['load'][1]:.1f}", metrics["load"][0] > ALERT["loadavg"]),
    ]

    for key, center, label, alert in ring_specs:
        val = metrics[key] if key != "load" else sum(metrics["load"]) / 3 * 25
        draw_ring(ax, center, val, label, alert, fg=style["fg"])

    # ─ Footer ─
    mood = "chill 🧃" if metrics["cpu"] < 50 else "watching 🔥"
    caption = caption_override or CAPTION_MOODS.get(theme, "")
    footer = f"{caption} • {metrics['hostname']} • up {metrics['uptime']//3600}h • {datetime.now().strftime('%H:%M')} • mood: {mood}"
    ax.text(1, -0.1, footer, ha="center", va="bottom", fontsize=8, color=style["fg"])

    # ─ Output ─
    buf = BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight", facecolor=style["bg"])
    plt.close(fig)
    buf.seek(0)
    return buf

# ─── Randomized Entry Point ──────────────────────────
def render_rings_random():
    metrics = get_sys_metrics()
    theme = random.choice(list(THEMES.keys()))
    caption = CAPTION_MOODS.get(theme, "")
    return render_rings(theme=theme, metrics=metrics, caption_override=caption)


