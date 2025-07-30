import asyncio, os, json
from datetime import datetime
import speedtest

from config import ADMIN_ID
from utils.helpers import get_uptime, save_result
from aiogram import Bot

STATE_PATH = "speedo_storage/autospeed_state.json"

AUTO_TASK = None
AUTO_ACTIVE = False
INTERVAL = 3600  # default (1 hour)

def load_autospeed_state():
    global AUTO_ACTIVE, INTERVAL
    if os.path.exists(STATE_PATH):
        try:
            with open(STATE_PATH) as f:
                data = json.load(f)
            AUTO_ACTIVE = data.get("active", False)
            INTERVAL = data.get("interval", 3600)
        except:
            pass

def save_autospeed_state():
    data = {
        "active": AUTO_ACTIVE,
        "interval": INTERVAL
    }
    os.makedirs(os.path.dirname(STATE_PATH), exist_ok=True)
    try:
        with open(STATE_PATH, "w") as f:
            json.dump(data, f)
    except:
        pass

async def run_autotest_and_notify(bot: Bot):
    try:
        st = speedtest.Speedtest()
        st.get_best_server()
        download = st.download() / 1_000_000
        upload = st.upload() / 1_000_000
        ping = st.results.ping
        timestamp = datetime.utcnow().isoformat()

        save_result(download, upload, ping, timestamp)

        caption = (
            f"⏰ <b>Auto Speedtest</b>\n"
            f"🕒 <b>Time:</b> {timestamp}\n"
            f"⬇️ <b>Download:</b> {download:.2f} Mbps\n"
            f"⬆️ <b>Upload:</b> {upload:.2f} Mbps\n"
            f"📶 <b>Ping:</b> {ping:.2f} ms\n"
            f"🖥 <b>VPS Uptime:</b> {get_uptime()}"
        )

        await bot.send_message(chat_id=ADMIN_ID, text=caption, parse_mode="HTML")
    except:
        pass

async def auto_monitor(bot: Bot):
    global AUTO_ACTIVE
    AUTO_ACTIVE = True
    save_autospeed_state()

    while AUTO_ACTIVE:
        await run_autotest_and_notify(bot)
        await asyncio.sleep(INTERVAL)

async def toggle_autospeed(bot: Bot, state: bool, hours: int = 1):
    global AUTO_TASK, AUTO_ACTIVE, INTERVAL
    INTERVAL = hours * 3600
    save_autospeed_state()

    if state and not AUTO_ACTIVE:
        AUTO_TASK = asyncio.create_task(auto_monitor(bot))
    elif not state and AUTO_ACTIVE:
        AUTO_ACTIVE = False
        if AUTO_TASK:
            AUTO_TASK.cancel()
            AUTO_TASK = None
        save_autospeed_state()

def get_autospeed_status() -> str:
    return (
        "📶 <b>AutoSpeed Monitor</b>\n"
        f"🔌 <b>Status:</b> {'Active ✅' if AUTO_ACTIVE else 'Inactive ❌'}\n"
        f"🕒 <b>Interval:</b> {INTERVAL // 3600} hour(s)"
    )


