import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.filters import Command
from speedtest import Speedtest
from config import TOKEN
from aiogram.client.default import DefaultBotProperties  # 👈 new import

bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)  # 👈 correct usage
)
dp = Dispatcher()

@dp.message(Command("speedtest"))
async def speedtest_handler(message: Message):
    await message.answer("Running speedtest... ⏳")
    st = Speedtest()
    st.get_best_server()
    download = st.download() / 1_000_000
    upload = st.upload() / 1_000_000
    ping = st.results.ping
    isp = st.config['client']['isp']
    result = (
        f"📡 ISP: {isp}\n"
        f"⬇️ Download: {download:.2f} Mbps\n"
        f"⬆️ Upload: {upload:.2f} Mbps\n"
        f"🕒 Ping: {ping:.2f} ms"
    )
    await message.answer(result)

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
