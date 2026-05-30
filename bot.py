import asyncio
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

from utils.anomaly import load_state, toggle_anomaly, ANOMALY_ACTIVE, THRESHOLD_LEVEL
from config import TOKEN, ADMIN_ID, THUMBNAIL_URL

# ✅ Modular routers
from handlers.diagnostics import router as diagnostics_router
from handlers.speedtest import router as speedtest_router
from handlers.admin import router as admin_router
from handlers.syschart import router as syschart_router
from handlers.loadrings import router as loadrings_router
from handlers.anomalywatch import router as anomaly_router
from handlers.netstatus import router as netstatus_router
from handlers.pwatch import router as pwatch_router


# 💡 Dispatcher setup
bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()
dp.include_router(diagnostics_router)
dp.include_router(speedtest_router)
dp.include_router(admin_router)
dp.include_router(syschart_router)
dp.include_router(loadrings_router)
dp.include_router(anomaly_router)
dp.include_router(netstatus_router)
dp.include_router(pwatch_router)


@dp.message(Command("start"))
async def start_handler(message: Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("🔒 Access Denied. Unauthorized terminal instance.")
        return

    await message.answer(
        "🛸 <b>Welcome to Speedo Core Engine v2.0</b> 🦔\n\n"
        "Your automated high-frequency telemetry system is armed and ready.\n\n"
        "<b>Available Core Executables:</b>\n"
        "├ /speedtest — 🚀 Execute high-precision official Ookla network metric run\n"
        "├ /lastspeed — 📦 Fetch latest recorded network state from log registry\n"
        "├ /healthscore — 🧠 Run holistic hardware and connectivity structural analysis\n"
        "├ /trend — 📈 Render localized visual throughput dispersion graph\n"
        "├ /monthlytrend — 📅 Render monthly macroeconomic performance drift chart\n"
        "├ /sysinfo — 📋 Pull immediate system specification array\n"
        "├ /netstatus — 🌐 Run deep active interface configuration socket diagnostic\n"
        "├ /anomalywatch — 🚨 Toggle active runtime performance deviation protection loop\n"
        "├ /pwatch — 🚀 Top 5 Resource-Heavy processes\n"
        "├ /syschart — 📊 Graphical telemetry panel(CPU USAGE, STORAGE..) with caption overlay\n"
        "└ /loadrings — 💍 Lord of the rings fidelity"
    )


# 🧠 System info helpers
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


# 🧪 Monitoring loop
from speedo_core.monitor import start_autospeed_monitor  # ✅ avoid shadowing


async def main():
    print("✅ Speedo deployed successfully, hedgehog 🦔.")
    await asyncio.sleep(15)
   
    # Load anomaly flags and logs from disk
    load_state()
    
    # Start background polling loops safely without blocking message processor
    asyncio.create_task(start_autospeed_monitor(bot))
    
    # Run long-polling session
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("🛑 Speedo Core shutdown successfully.")
