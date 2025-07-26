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

def mask_ip(ip: str) -> str:
    segments = ip.split(".")
    masked_segments = []
    for seg in segments:
        masked = ""
        for ch in seg:
            if ch.isdigit() and random.random() < 0.5:
                masked += random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
            else:
                masked += ch
        masked_segments.append(masked)
    return ".".join(masked_segments)

def save_result(download, upload, ping, timestamp):
    os.makedirs("results", exist_ok=True)
    data = {
        "timestamp": timestamp,
        "download": round(download, 2),
        "upload": round(upload, 2),
        "ping": round(ping, 2)
    }
    existing = []
    if os.path.exists(RESULTS_LOG):
        with open(RESULTS_LOG) as f:
            existing = json.load(f)
    existing.append(data)
    with open(RESULTS_LOG, "w") as f:
        json.dump(existing[-30:], f, indent=2)

def generate_plot():
    if not os.path.exists(RESULTS_LOG):
        return None
    with open(RESULTS_LOG) as f:
        data = json.load(f)
    timestamps = [datetime.fromisoformat(d["timestamp"]) for d in data]
    downloads = [d["download"] for d in data]
    uploads = [d["upload"] for d in data]
    plt.figure(figsize=(10, 5))
    plt.plot(timestamps, downloads, label="Download (Mbps)", color="blue")
    plt.plot(timestamps, uploads, label="Upload (Mbps)", color="green")
    plt.legend()
    plt.title("Speed Trends")
    plt.xlabel("Time")
    plt.ylabel("Mbps")
    plt.grid()
    plt.tight_layout()
    plt.savefig(TREND_IMAGE)
    return TREND_IMAGE

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
