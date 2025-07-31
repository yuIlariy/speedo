import psutil

def top_processes(limit=5):
    """Return top N processes sorted by RAM + CPU usage."""
    procs = []
    for p in psutil.process_iter(['pid', 'name', 'memory_percent', 'cpu_percent']):
        try:
            info = p.info
            pid = info['pid']
            name = info['name'] or '—'
            mem = info['memory_percent'] or 0
            cpu = info['cpu_percent'] or 0
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


