import re, datetime, random
from dateutil import tz
import geoip2.database

GEO_READER = geoip2.database.Reader("GeoLite2-City.mmdb")  # Adjust path if needed

THEMES = [
    {"success": "🟢🌋", "fail": "🔴⚡", "caption": "Login from {country} 🌍 — {user} @ {time}"},
    {"success": "✅🔥", "fail": "❌💀", "caption": "{user} breached from {country} @ {time}"},
    {"success": "🛡️🧘", "fail": "🧨🕷️", "caption": "Access attempt by {user} — {status} from {country}"},
]

def parse_auth_log(path="/var/log/auth.log", max_lines=100):
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
    try:
        response = GEO_READER.city(ip)
        flag = response.country.iso_code
        return f"{response.country.name} {flag}"
    except:
        return "Unknown"


