import psutil, socket, subprocess
from datetime import datetime

def get_network_panel():
    interfaces = psutil.net_if_addrs()
    stats = psutil.net_io_counters(pernic=True)
    uptime = psutil.boot_time()
    now = datetime.utcnow()

    summary = "🌐 **Network Pulse Panel**\n\n"

    for iface in interfaces:
        ip4 = ip6 = mac = "—"
        for addr in interfaces[iface]:
            if addr.family.name == 'AF_INET':
                ip4 = addr.address
            elif addr.family.name == 'AF_INET6':
                ip6 = addr.address
            elif addr.family.name == 'AF_PACKET':
                mac = addr.address

        rx = stats[iface].bytes_recv // 1024
        tx = stats[iface].bytes_sent // 1024

        status_line = f"""
🔌 `{iface}`
▸ IPv4: `{ip4}` / IPv6: `{ip6}`
▸ MAC: `{mac}`
📥 RX: `{rx} KB` / 📤 TX: `{tx} KB`
"""
        summary += status_line

    summary += f"\n🕰️ Uptime: `{(now - datetime.utcfromtimestamp(uptime)).days} days`\n"
    summary += "\n📶 **Ping Test**: "

    try:
        result = subprocess.run(["ping", "-c", "1", "8.8.8.8"], stdout=subprocess.PIPE)
        if result.returncode == 0:
            summary += "🟢 Connected"
        else:
            summary += "🔴 No response"
    except:
        summary += "⚠️ Ping failed"

    return summary


