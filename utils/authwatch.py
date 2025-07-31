import re, datetime, random, requests
from aiogram import Bot
from config import ADMIN_ID

THEMES = [
    {"success": "🟢🌋", "fail": "🔴⚡", "caption": "Login from {country} 🌍 — {user} @ {time}"},
    {"success": "✅🔥", "fail": "❌💀", "caption": "{user} breached from {country} @ {time}"},
    {"success": "🛡️🧘", "fail": "🧨🕷️", "caption": "Access attempt by {user} — {status} from {country}"},
]

def parse_auth_log(path="/var/log/auth.log", max_lines=50):
    try:
        with open(path, "r") as f:
            lines = f.readlines()[-max_lines:]
    except FileNotFoundError:
        return []

    entries = []
    for line in lines:
        if "sshd" not in line: continue
        status = "success" if "Accepted" in line else "failed" if "Failed" in line else None
        if not status: continue

        ip_match = re.search(r"(\d{1,3}\.){3}\d{1,3}", line)
        user_match = re.search(r"user (\w+)", line)
        ip = ip_match.group() if ip_match else "?"
        user = user_match.group(1) if user_match else "?"

        time_utc = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        country = lookup_country(ip)
        theme = random.choice(THEMES)
        emoji = theme["success"] if status == "success" else theme["fail"]
        caption = theme["caption"].format(user=user, country=country, time=time_utc, status=status)

        entries.append({
            "status": status,
            "user": user,
            "ip": ip,
            "country": country,
            "time": time_utc,
            "emoji": emoji,
            "caption": caption
        })
    return entries

def lookup_country(ip):
    if ip == "?" or ip.startswith("127."): return "Localhost 🌐"
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}", timeout=3)
        if r.status_code == 200:
            data = r.json()
            country = data.get("country", "Unknown")
            cc = data.get("countryCode", "")
            flag = f" {cc}" if cc else ""
            return f"{country}{flag}"
    except:
        pass
    return "Unknown"

async def notify_admin(bot: Bot):
    entries = parse_auth_log()
    if not entries:
        return
    latest = entries[-1]
    summary = f"{latest['emoji']} {latest['caption']}"
    await bot.send_message(chat_id=ADMIN_ID, text=summary)


