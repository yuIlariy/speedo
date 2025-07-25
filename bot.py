import logging
from aiogram import Bot, Dispatcher, executor, types
from config import TOKEN, LOG_FILE
from handlers.speedtest_handler import handle_speedtest

logging.basicConfig(filename=LOG_FILE, level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['speedtest'])
async def speedtest_command(message: types.Message):
    await handle_speedtest(message)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
