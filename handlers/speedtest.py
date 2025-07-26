from aiogram import types
from utils.speedtest import run_speedtest

async def handle_speedtest(message: types.Message):
    await message.reply("Running speedtest... ⏳")
    result = run_speedtest()
    await message.reply(result)
