import asyncio, os, json
from datetime import datetime, timedelta
import speedtest
from aiogram import Bot
from config import ADMIN_ID
from utils.helpers import get_uptime, save_result

STATE_PATH = "speedo_storage/autospeed_state.json"

AUTO_TASK = None
AUTO_LAST_RUN = None
INTERVAL = 3600  # 👈 Hardcoded to 1 hour

def save_autospeed_state():
    data = {
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
            f"⏰ <b>Speedo Auto Speedtest</b>\n"
            f"🕒 <b>Time:</b> {AUTO_LAST_RUN.isoformat()}\n"
            f"⬇️ <b>Download:</b> {download:.2f} Mbps\n"
            f"⬆️ <b>Upload:</b> {upload:.2f} Mbps\n"
            f"📶 <b>Ping:</b> {ping:.2f} ms\n"
            f"🖥 <b>VPS Uptime:</b> {get_uptime()}"
        )
        await bot.send_message(ADMIN_ID, caption)
    except:
        pass
    finally:
        save_autospeed_state()

async def start_autospeed_monitor(bot: Bot):
    while True:
        await perform_speedtest(bot)
        await asyncio.sleep(INTERVAL)

