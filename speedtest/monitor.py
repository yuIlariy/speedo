import asyncio
from datetime import datetime
from speedtest import speedtest

from config import ADMIN_ID
from utils.helpers import get_uptime, save_result
from aiogram import Bot

AUTO_INTERVAL = 3600  # seconds

async def run_autotest_and_notify(bot: Bot):
    st = Speedtest()
    st.get_best_server()
    download = st.download() / 1_000_000
    upload = st.upload() / 1_000_000
    ping = st.results.ping
    timestamp = datetime.utcnow().isoformat()

    save_result(download, upload, ping, timestamp)

    caption = (
        f"⏰ <b>Hourly Auto Speedtest</b>\n"
        f"🕒 <b>Time:</b> {timestamp}\n"
        f"⬇️ <b>Download:</b> {download:.2f} Mbps\n"
        f"⬆️ <b>Upload:</b> {upload:.2f} Mbps\n"
        f"📶 <b>Ping:</b> {ping:.2f} ms\n"
        f"🖥 <b>VPS Uptime:</b> {get_uptime()}"
    )

    try:
        await bot.send_message(chat_id=ADMIN_ID, text=caption)
    except Exception:
        pass  # Early startup failure okay

async def auto_monitor(bot: Bot):
    while True:
        await run_autotest_and_notify(bot)
        await asyncio.sleep(AUTO_INTERVAL)


