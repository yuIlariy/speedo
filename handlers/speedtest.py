from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from datetime import datetime
from speedtest import Speedtest

from config import ADMIN_ID, THUMBNAIL_URL
from utils.helpers import get_uptime, mask_ip, save_result
from utils.helpers import generate_plot

router = Router()

@router.message(Command("speedtest"))
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


import json
from config import RESULTS_LOG, ADMIN_ID

@router.message(Command("lastspeed"))
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


@router.message(Command("healthscore"))
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

        # ⚙️ Scoring logic
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



import matplotlib.pyplot as plt
from aiogram.types.input_file import FSInputFile
import random

@router.message(Command("monthlytrend"))
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

        # 🧠 Simple trend classification
        trend = "unknown"
        if max(uploads) < 2 or max(downloads) < 20:
            trend = "dip"
        elif min(uploads) > 15 and min(downloads) > 50:
            trend = "smooth"
        elif uploads[-1] - uploads[0] > 20:
            trend = "spike"
        elif max(uploads) - min(uploads) < 1 and max(downloads) - min(downloads) < 5:
            trend = "stagnant"

        captions = {
            "spike": [
                "🚀 Monthly speed spike in motion. We’ve got lift-off 📅",
                "📈 Performance shot up this month. Keep the trend alive!",
                "⚡️ Speed burst spotted. ISP finally behaving?"
            ],
            "dip": [
                "🌪️ Monthly turbulence detected. Hold your packets tight!",
                "📉 Consistency took a holiday this month.",
                "⚠️ Not our best month. Maybe it's time to switch plans?"
            ],
            "smooth": [
                "✅ This month’s speed graph is looking crisp.",
                "🧘‍♂️ Smooth performance all through the month.",
                "📊 Monthly zen mode activated. We love stability."
            ],
            "stagnant": [
                "📎 Not much movement this month… just humming along.",
                "📆 Flat graph, flat vibes. Is no change a good thing?",
                "😐 Stability or stagnation? You decide."
            ],
            "unknown": [
                "📅 Here’s the speed trend for this month. Interpret wisely!",
                "🧐 Monthly graph incoming. Tell me what you see.",
                "🧾 Latest monthly analytics, hot off the VPS!"
            ]
        }

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
        caption = random.choice(captions.get(trend, captions["unknown"]))
        await message.answer_photo(photo=photo, caption=caption)

    except Exception as e:
        await message.answer(f"⚠️ Error plotting monthly trend\n{e}")


import matplotlib.pyplot as plt
from aiogram.types.input_file import FSInputFile
import random

@router.message(Command("trend"))
async def trend_handler(message: Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("🚫 Admin only.")
        return

    def generate_plot(return_summary=False):
        try:
            with open(RESULTS_LOG, "r") as f:
                data = json.load(f)
            recent = data[-30:]  # Adjust as needed

            timestamps = [datetime.fromisoformat(d["timestamp"]) for d in recent]
            downloads = [d["download"] for d in recent]
            uploads = [d["upload"] for d in recent]

            summary = "unknown"
            if max(uploads) < 2 or max(downloads) < 20:
                summary = "dip"
            elif min(uploads) > 15 and min(downloads) > 50:
                summary = "smooth"
            elif uploads[-1] - uploads[0] > 20:
                summary = "spike"
            elif max(uploads) - min(uploads) < 1 and max(downloads) - min(downloads) < 5:
                summary = "stagnant"

            plt.figure(figsize=(10, 5))
            plt.plot(timestamps, downloads, label="⬇️ Download", color="blue", marker="o")
            plt.plot(timestamps, uploads, label="⬆️ Upload", color="green", marker="o")
            plt.legend()
            plt.title("📈 Speed Trend")
            plt.xlabel("Time")
            plt.ylabel("Mbps")
            plt.grid()
            plt.tight_layout()

            path = "results/speedplot.png"
            plt.savefig(path)

            return (path, summary) if return_summary else path
        except Exception:
            return (None, "error") if return_summary else None

    path, trend_summary = generate_plot(return_summary=True)

    if path:
        photo = FSInputFile(path)

        caption_bank = {
            "spike": [
                "🚨 Speed surge detected! Someone paid the ISP bill? 📈",
                "🎢 That spike tho… hold on to your packets!",
                "🔋 Throughput explosion. We hit warp speed ⚡"
            ],
            "dip": [
                "⚠️ Speed dip spotted. Time to run a pingtest?",
                "🕳️ That trough hurts. Network ghost in the wires?",
                "🌪️ Bottleneck vibes. Who stole our Mbps?"
            ],
            "stagnant": [
                "😐 Flatline detected. Stability or staleness?",
                "🧊 Speed’s been chilling. No news, good news?",
                "📎 Graph’s stuck — just like your downloads?"
            ],
            "smooth": [
                "✅ Stable speeds. Graph looking clean!",
                "🧘‍♂️ Network in zen mode. Nothing out of place 🌀",
                "📊 That’s some VPS consistency right there!"
            ],
            "unknown": [
                "📈 Latest trend — let’s dissect it together!",
                "🧐 Speed story over time. Any surprises?",
                "⚙️ Here's how the network’s been behaving lately..."
            ],
            "error": [
                "⚠️ Couldn’t analyze trend, but here’s the graph.",
                "💥 Plot rendered, analysis went rogue.",
                "🤖 Chart saved, but summary’s scrambled."
            ]
        }

        caption = random.choice(caption_bank.get(trend_summary, caption_bank["unknown"]))
        await message.answer_photo(photo=photo, caption=caption)
    else:
        await message.answer("⚠️ No results found to plot.")


