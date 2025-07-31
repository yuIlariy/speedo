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
    """Create formatted caption panel with emoji and aligned usage."""
    lines = ["🚀 = CPU • 💾 = RAM\n"]
    for pid, name, mem, cpu in proc_list:
        mood = "🟢" if mem + cpu > 20 else "🟡" if mem + cpu > 10 else "🔴"
        lines.append(f"{mood} `{name}` 🚀 {cpu:.1f}% | 💾 {mem:.1f}% | PID `{pid}`")
    return "\n".join(lines)


