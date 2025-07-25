import asyncio
import random
import json
import os
import subprocess
from datetime import datetime
import matplotlib.pyplot as plt
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command
from aiogram.client.default import DefaultBotProperties
from speedtest import Speedtest
from config import TOKEN, ADMIN_ID, THUMBNAIL_URL

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
    await message.answer(
        "👋 Welcome, master of machines!\n\n"
        "⚙️ Your VPS companion is standing by.\n"
        "💡 Try /speedtest, /trend, /lastspeed, /healthscore, or /sysinfo\n\n"
        "📈 Your server. Your rules. Your graphs.👑"
    )

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

    save_result(download, upload, ping, timestamp)

    server = st.get_best_server()
    client = st.config['client']
    masked_ip = mask_ip(client['ip'])
    uptime = get_uptime()

    caption = (
        f"<b>🚀 SPEEDTEST INFO 🚀</b>\n"
        f"├ Upload: {upload:.2f} MB/s\n"
        f"├ Download: {download:.2f} MB/s\n"
        f"├ Ping: {ping:.3f} ms\n"
        f"├ Time:\n{timestamp}\n"
        f"├ VPS Uptime: {uptime}\n"
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


@dp.message(Command("lastspeed"))
async def lastspeed_handler(message: Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("🚫 Admin only.")
        return

    try:
        with open(RESULTS_LOG) as f:
            data = json.load(f)
        latest = data[-1]

        reply = (
            f"📦 <b>Latest Speed Test</b>\n"
            f"🕒 <b>Time:</b> {latest['timestamp']}\n"
            f"⬇️ <b>Download:</b> {latest['download']} Mbps\n"
            f"⬆️ <b>Upload:</b> {latest['upload']} Mbps\n"
            f"📶 <b>Ping:</b> {latest['ping']} ms"
        )
        await message.answer(reply)
    except Exception as e:
        await message.answer(f"⚠️ Could not read last result.\nError: {e}")



@dp.message(Command("healthscore"))
async def healthscore_handler(message: Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("🚫 Admin only.")
        return

    try:
        with open(RESULTS_LOG) as f:
            latest = json.load(f)[-1]

        dl = latest["download"]
        ul = latest["upload"]
        ping = latest["ping"]
        score = 0

        # Scoring logic
        score += 2 if dl >= 100 else 1 if dl >= 50 else 0
        score += 2 if ul >= 30 else 1 if ul >= 10 else 0
        score += 2 if ping <= 20 else 1 if ping <= 50 else 0

        verdicts = {
            6: "💎 Perfect: VPS is blazing.",
            5: "⚡ Great: Smooth and responsive.",
            4: "📈 Decent: No bottlenecks detected.",
            3: "📉 Moderate: Might struggle under load.",
            2: "🪫 Weak: Below ideal performance.",
            1: "🛑 Poor: Network degraded.",
            0: "❌ Offline or unusable."
        }

        verdict = verdicts.get(score, "🌐 Unknown status.")
        reply = (
            f"<b>🧠 Health Score:</b> {score}/6\n"
            f"{verdict}\n\n"
            f"⬇️ <b>Download:</b> {dl} Mbps\n"
            f"⬆️ <b>Upload:</b> {ul} Mbps\n"
            f"📶 <b>Ping:</b> {ping} ms"
        )
        await message.answer(reply)
    except Exception as e:
        await message.answer(f"⚠️ Error calculating health score.\n{e}")



@dp.message(Command("monthlytrend"))
async def monthlytrend_handler(message: Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("🚫 Admin only.")
        return

    now = datetime.utcnow()
    current_month = now.month
    current_year = now.year

    try:
        with open(RESULTS_LOG) as f:
            data = json.load(f)

        month_data = [
            d for d in data
            if datetime.fromisoformat(d["timestamp"]).month == current_month
            and datetime.fromisoformat(d["timestamp"]).year == current_year
        ]

        if not month_data:
            await message.answer("📭 No tests found for this month.")
            return

        timestamps = [datetime.fromisoformat(d["timestamp"]) for d in month_data]
        downloads = [d["download"] for d in month_data]
        uploads = [d["upload"] for d in month_data]

        plt.figure(figsize=(10, 5))
        plt.plot(timestamps, downloads, label="Download (Mbps)", color="blue")
        plt.plot(timestamps, uploads, label="Upload (Mbps)", color="green")
        plt.legend()
        plt.title("📅 Monthly Speed Trends")
        plt.xlabel("Time")
        plt.ylabel("Mbps")
        plt.grid()
        plt.tight_layout()

        monthly_path = "results/speedplot_monthly.png"
        plt.savefig(monthly_path)

        photo = FSInputFile(monthly_path)
        await message.answer_photo(photo=photo)
    except Exception as e:
        await message.answer(f"⚠️ Error plotting monthly trend\n{e}")


@dp.message(Command("exportlog"))
async def exportlog_handler(message: Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("🚫 Admin only.")
        return

    if not os.path.exists(RESULTS_LOG):
        await message.answer("📭 Log file is missing.")
        return

    document = FSInputFile(RESULTS_LOG)
    await message.answer_document(document, caption="🧾 Log dump: speedlog.json")


@dp.message(Command("pingtest"))
async def pingtest_handler(message: Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("🚫 Admin only.")
        return

    try:
        output = subprocess.check_output("ping -c 5 8.8.8.8", shell=True).decode()
        loss_line = [line for line in output.splitlines() if "packet loss" in line]
        latency_line = [line for line in output.splitlines() if "min/avg/max" in line]

        loss = loss_line[0].strip() if loss_line else "N/A"
        latency = latency_line[0].strip() if latency_line else "N/A"

        verdict = "🔥 Stable" if "0% packet loss" in loss else (
            "⚠️ Okay" if "1%" in loss or "2%" in loss else "❌ Poor"
        )

        reply = (
            f"<b>🧪 Ping Test (8.8.8.8)</b>\n"
            f"{verdict}\n\n"
            f"📡 {loss}\n"
            f"📶 {latency}"
        )
        await message.answer(reply)
    except Exception as e:
        await message.answer(f"⚠️ Ping test failed\n{e}")



@dp.message(Command("trend"))
async def trend_handler(message: Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("🚫 Admin only.")
        return

    path = generate_plot()
    if path:
        photo = FSInputFile(path)
        await message.answer_photo(photo=photo)
    else:
        await message.answer("⚠️ No results found to plot.")

@dp.message(Command("sysinfo"))
async def sysinfo_handler(message: Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("🚫 Admin only.")
        return
    info = get_sysinfo()
    await message.answer(f"<b>🚨 VPS System Info</b>\n\n{info}")

async def main():
    print("✅ Speedo deployed successfully, hedgehog 🤩.")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())


# 🚀 Speedo Bot — Telegram VPS Speedtest
# 🧠 Extended by Yuilariy x MS Copilot
# 📎 Original repo: https://github.com/yuIlariy/speedo
# 🤩 Fork it. Use it. Credit it. Rule it 👑
