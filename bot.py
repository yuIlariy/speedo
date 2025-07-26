import asyncio
import random
import json
import psutil
import os
import subprocess
from datetime import datetime
import matplotlib.pyplot as plt
from aiogram import Bot, Dispatcher
from aiogram.filters.command import CommandObject
from aiogram.enums import ParseMode
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command
from aiogram.client.default import DefaultBotProperties
from speedtest import Speedtest
from config import TOKEN, ADMIN_ID, THUMBNAIL_URL
from aiogram import Dispatcher, Bot
from handlers.diagnostics import router as diagnostics_router
from handlers.speedtest import router as speedtest_router
from handlers.admin import router as admin_router
from handlers import speedtest

dp.include_router(speedtest.router)
dp.include_router(diagnostics_router)
dp.include_router(speedtest_router)
dp.include_router(admin_router)

bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

RESULTS_LOG = "results/speedlog.json"
TREND_IMAGE = "results/speedplot.png"


def get_sysinfo():
    def run(cmd): return subprocess.check_output(cmd, shell=True).decode().strip()
    info = {
        "☁️ CPU": run("lscpu | grep 'Model name' | awk -F: '{print $2}'").strip(),
        "⏱️ Uptime": run("uptime -p"),
        "💾 Disk": run("df -h / | tail -1 | awk '{print $3 \"/\" $2 \" used\"}'"),
        "📦 Memory": run("free -h | grep Mem | awk '{print $3 \"/\" $2 \" used\"}'"),
        "📊 Load Average": run("uptime | awk -F: '{print $NF}'")
    }
    return "\n".join([f"{k}: {v}" for k, v in info.items()])

def get_uptime():
    return subprocess.check_output("uptime -p", shell=True).decode().strip()

@dp.message(Command("start"))
async def start_handler(message: Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("🚫 This bot is restricted to admin use only.")
        return

    thumbnail_url = "https://telegra.ph/file/ec17880d61180d3312d6a.jpg"
    await message.answer_photo(
        photo=thumbnail_url,
        caption=(
            "<b>👋 Welcome, master of machines!</b>\n\n"
            "🚀 Speedo Bot is locked, loaded, and watching your VPS like royalty 👑\n\n"
            "💬 Need help? Use /help to view your full command arsenal.\n\n"
            "📈 Graphs, logs, health checks — all under your control."
        )
    )

@dp.message(Command("help"))
async def help_handler(message: Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("🚫 Help is reserved for sysadmin eyes only.")
        return

    thumbnail_url = "https://telegra.ph/file/ec17880d61180d3312d6a.jpg"
    await message.answer_photo(
        photo=thumbnail_url,
        caption=(
            "<b>🧾 Command Panel — Speedo NOC Suite 👑</b>\n\n"
            "/speedtest — 🚨 run speedtest\n"
            "/sysinfo — ☁️ Sys info\n"
            "/lastspeed — ⚡ latest speedtest\n"
            "/trend — 📈 graphical trend for upto 30 recent tests 📈\n"
            "/healthscore — 🎖️ Precious VPS speed & ping healthscore 👑\n"
            "/pingtest — 🚀 Ping Check on default targets or specify the target IP or address 🎈\n"
            "/exportlog — 🧾 speedtest Log dump\n"
            "/monthlytrend — 📈 monthly trend speed graph 📉\n"
            "/bootcheck — 🚀 VPS Boot Check ⚡"
        )
    )





from speedtest.monitor import auto_monitor

async def main():
    print("✅ Speedo deployed successfully, hedgehog 🤩.")
    await asyncio.sleep(15)
    asyncio.create_task(auto_monitor(bot))
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())


# 🚀 Speedo Bot — Telegram VPS Speedtest
# 🧠 Extended by Yuilariy x MS Copilot
# 📎 Original repo: https://github.com/yuIlariy/speedo
# 🤩 Fork it. Use it. Credit it. Rule it 👑
