import psutil

def top_processes(limit=5):
    """Return top N processes sorted by true system-relative RAM + CPU usage."""
    procs = []
    cpu_count = psutil.cpu_count(logical=True)
    ram_total = psutil.virtual_memory().total

    for p in psutil.process_iter(['pid', 'name']):
        try:
            pid = p.pid
            name = p.name() or '—'
            cpu_raw = p.cpu_percent(interval=0.1)
            ram_raw = p.memory_info().rss

            # ✅ Normalize to system-wide percentages
            cpu = (cpu_raw / (100 * cpu_count)) * 100
            mem = (ram_raw / ram_total) * 100

            procs.append((pid, name, mem, cpu))
        except:
            continue

    procs.sort(key=lambda x: (x[2] + x[3]), reverse=True)
    return procs[:limit]

def format_process_panel(proc_list):
    """Create formatted caption panel with emoji and aligned usage + mood tags."""
    lines = []

    for pid, name, mem, cpu in proc_list:
        total = mem + cpu
        if total > 50:
            mood = "🌋 Overloaded"
            icon = "🔴"
        elif total > 20:
            mood = "🔥 Active"
            icon = "🟢"
        elif total > 10:
            mood = "🌡 Moderate"
            icon = "🟡"
        else:
            mood = "❄️ Chill"
            icon = "⚪"

        lines.append(f"{icon} `{name}` 🚀 {cpu:.1f}% | 💾 {mem:.1f}% | PID `{pid}` • {mood}")

    return "\n".join(lines)


