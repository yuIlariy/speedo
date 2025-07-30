import psutil, subprocess, socket
from datetime import datetime

def get_network_panel():
    interfaces = psutil.net_if_addrs()
    stats = psutil.net_io_counters(pernic=True)
    uptime = psutil.boot_time()
    now = datetime.utcnow()

    summary = "🌐 **Network Pulse Panel**\n\n"
    health_emojis = []

    for iface in interfaces:
        ip4 = ip6 = mac = "—"
        for addr in interfaces[iface]:
            if addr.family.name == 'AF_INET':
                ip4 = addr.address
            elif addr.family.name == 'AF_INET6':
                ip6 = addr.address
            elif addr.family.name == 'AF_PACKET':
                mac = addr.address

        rx = stats.get(iface).bytes_recv // 1024 if iface in stats else 0
        tx = stats.get(iface).bytes_sent // 1024 if iface in stats else 0

        # Emoji status based on TX/RX
        mood = "🟢" if rx > 200 and tx > 100 else "🟡" if rx > 50 or tx > 50 else "🔴"
        health_emojis.append(mood)

        summary += f"""\
{mood} `{iface}`
▸ IP: `{ip4}` | MAC: `{mac}`
▸ RX: `{rx} KB` / TX: `{tx} KB`\n"""

    # Ping check to confirm net connectivity
    try:
        result = subprocess.run(["ping", "-c", "1", "8.8.8.8"], stdout=subprocess.DEVNULL)
        ping_status = "🟢 Ping OK"
        health_emojis.append("🟢")
    except:
        ping_status = "🔴 Ping Fail"
        health_emojis.append("🔴")

    uptime_delta = now - datetime.utcfromtimestamp(uptime)
    days = uptime_delta.days
    hours = uptime_delta.seconds // 3600

    summary += f"\n📶 {ping_status}\n"
    summary += f"🕰️ Uptime: `{days}d {hours}h`\n"
    summary += f"\n👻 Health Summary: {' '.join(health_emojis)}"

    return summary


