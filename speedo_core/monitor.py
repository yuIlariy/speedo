import asyncio, os, json, re
from datetime import datetime, timedelta
import speedtest

from config import ADMIN_ID
from utils.helpers import get_uptime, save_result
from aiogram import Bot

STATE_PATH = "speedo_storage/autospeed_state.json"

AUTO_TASK = None
AUTO_ACTIVE = False
AUTO_LAST_RUN = None
INTERVAL = 3600  # default = 1 hour

def parse_duration(raw: str) -> int:
    """Parses '2h', '30m', '45s', or fallback to seconds."""
    match = re.fullmatch(r"(\d+)([hmsHMS]?)", raw.strip())
    if not match:
        return 3600
    val, unit = match.groups()
    val = int(val)
    unit = unit.lower()
    return val * 3600 if unit == "h" else val * 60 if unit == "m" else val

def load_autospeed_state():
    global AUTO_ACTIVE, INTERVAL, AUTO_LAST_RUN
    if os.path.exists(STATE_PATH):
        try:
            with open(STATE_PATH) as f:
                data = json.load(f)
            AUTO_ACTIVE = data.get("active", False)
            INTERVAL = data.get("interval", 3600)
            ts = data.get("last_run")
            if ts:
                AUTO_LAST_RUN = datetime.fromisoformat(ts)
        except:
            pass

def save_autospeed_state():
    data = {
        "active": AUTO_ACTIVE,
        "interval": INTERVAL,
        "last_run": AUTO_LAST_RUN.isoformat() if AUTO_LAST_RUN else None
    }
    os.makedirs(os.path.dirname(STATE_PATH), exist_ok=True)
    try:
        with open(STATE_PATH, "w") as f:
            json.dump(data, f)
    except:
        pass

async def perform_speedtest(bot: Bot):
    global AUTO_LAST_RUN
    try:
        st = speedtest.Speedtest()
        st.get_best_server()
        download = st.download() / 1_000_000
        upload = st.upload() / 1_000_000
        ping = st.results.ping
        AUTO_LAST_RUN = datetime.utcnow()
        save_result(download, upload, ping, AUTO_LAST_RUN.isoformat())

        caption = (
            f"⏰ <b>Auto Speedtest</b>\n"
            f"🕒 <b>Time:</b> {AUTO_LAST_RUN.isoformat()}\n"
            f"⬇️ <b>Download:</b> {download:.2f} Mbps\n"
            f"⬆️ <b>Upload:</b> {upload:.2f} Mbps\n"
            f"📶 <b>Ping:</b> {ping:.2f} ms\n"
            f"🖥 <b>VPS Uptime:</b> {get_uptime()}"
        )
        await bot.send_message(ADMIN_ID, caption, parse_mode="HTML")
    except Exception as e:
        try:
            await bot.send_message(ADMIN_ID, f"⚠️ Speedtest error: `{str(e)}`", parse_mode="Markdown")
        except:
            pass
    finally:
        save_autospeed_state()

async def auto_monitor(bot: Bot):
    while AUTO_ACTIVE:
        await asyncio.sleep(INTERVAL)
        await perform_speedtest(bot)

async def toggle_autospeed(bot: Bot, state: bool, duration_str: str = "1h"):
    global AUTO_TASK, AUTO_ACTIVE, INTERVAL
    INTERVAL = parse_duration(duration_str)

    if state and not AUTO_ACTIVE:
        AUTO_ACTIVE = True
        bot.loop.create_task(perform_speedtest(bot))      # ✅ Instant run
        AUTO_TASK = bot.loop.create_task(auto_monitor(bot))  # ✅ Start background loop
    elif not state and AUTO_ACTIVE:
        AUTO_ACTIVE = False
        if AUTO_TASK:
            AUTO_TASK.cancel()
            AUTO_TASK = None

    save_autospeed_state()

def get_autospeed_status() -> str:
    eta = "Not scheduled yet"
    if AUTO_ACTIVE and AUTO_LAST_RUN:
        next_eta = AUTO_LAST_RUN + timedelta(seconds=INTERVAL)
        eta = next_eta.strftime("%Y-%m-%d %H:%M:%S UTC")

    readable = (
        f"{INTERVAL // 3600}h" if INTERVAL >= 3600 else
        f"{INTERVAL // 60}m" if INTERVAL >= 60 else
        f"{INTERVAL}s"
    )

    return (
        "📶 <b>AutoSpeed Monitor</b>\n"
        f"🔌 <b>Status:</b> {'Active ✅' if AUTO_ACTIVE else 'Inactive ❌'}\n"
        f"🕒 <b>Interval:</b> {readable}\n"
        f"🗓️ <b>Next Run:</b> {eta}"
    )


