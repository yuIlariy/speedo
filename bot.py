import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.client.default import DefaultBotProperties
from speedtest import Speedtest
from config import TOKEN, ADMIN_ID, THUMBNAIL_URL
from datetime import datetime

bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

def mask_ip(ip: str) -> str:
    # Mask IP as per pattern: 68.3R.358.16S
    segments = ip.split(".")
    suffixes = ['R', 'S', 'K', 'Z']
    masked = [f"{seg}{suffixes[i]}" for i, seg in enumerate(segments)]
    return ".".join(masked)

@dp.message(Command("start"))
async def start_handler(message: Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("🚫 This bot is restricted to admin use only.")
        return
    await message.answer("👋 Hello! Send /speedtest to check VPS performance.")

@dp.message(Command("speedtest"))
async def speedtest_handler(message: Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("🚫 This command is for admin only.")
        return

    await message.answer("Running speedtest... ⏳")
    st = Speedtest()
    st.get_best_server()
    download = st.download() / 1_000_000
    upload = st.upload() / 1_000_000
    ping = st.results.ping
    timestamp = datetime.utcnow().isoformat()

    server = st.get_best_server()
    client = st.config['client']
    masked_ip = mask_ip(client['ip'])

    caption = (
        f"<b>🚀 SPEEDTEST INFO 🚀</b>\n"
        f"├ Upload: {upload:.2f} MB/s\n"
        f"├ Download: {download:.2f} MB/s\n"
        f"├ Ping: {ping:.3f} ms\n"
        f"├ Time:\n{timestamp}\n"
        f"├ Data Sent: {st.results.bytes_sent / 1_000_000:.2f}MB\n"
        f"├ Data Received: {st.results.bytes_received / 1_000_000:.2f}MB\n\n"
        f"<b>🌐 SPEEDTEST SERVER 🌐</b>\n"
        f"├ Name: {server['name']}\n"
        f"├ Country: {server['country']}, {server['cc']}\n"
        f"├ Sponsor: {server['sponsor']}\n"
        f"├ Latency: {server['latency']:.3f} ms\n"
        f"├ Latitude: {server['lat']}\n"
        f"├ Longitude: {server['lon']}\n\n"
        f"<b>👤 CLIENT DETAILS 👤</b>\n"
        f"├ IP Address: {masked_ip}\n"
        f"├ Latitude: {client['lat']}\n"
        f"├ Longitude: {client['lon']}\n"
        f"├ Country: {client['country']}\n"
        f"├ ISP: {client['isp']}\n\n"
        f"<b>🏆Powered by NAm.🚨</b>"
    )

    await message.answer_photo(photo=THUMBNAIL_URL, caption=caption)

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
