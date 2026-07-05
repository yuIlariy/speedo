from datetime import datetime
import matplotlib.pyplot as plt
import json
import random
import asyncio
import aiohttp
from aiogram.filters import Command
from aiogram.types.input_file import FSInputFile

from aiogram import Router
from aiogram.types import Message

from config import ADMIN_ID, THUMBNAIL_URL, RESULTS_LOG
from utils.helpers import get_uptime, mask_ip, save_result, generate_plot

router = Router()

async def fetch_ip_geo(ip_address: str) -> dict:
    """Asynchronously fetch IP geolocation data."""
    if not ip_address or ip_address == '0.0.0.0':
        return {}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"http://ip-api.com/json/{ip_address}") as response:
                if response.status == 200:
                    return await response.json()
    except Exception:
        pass
    return {}

@router.message(Command("speedtest"))
async def speedtest_handler(message: Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("🚫 This command is for admin only.")
        return

    await message.answer("Running official Ookla speedtest... ⏳")

    try:
        # Run official Ookla speedtest CLI asynchronously 
        process = await asyncio.create_subprocess_exec(
            'speedtest', '--accept-license', '--accept-gdpr', '-f', 'json',
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        
        if process.returncode != 0:
            error_msg = stderr.decode('utf-8').strip() or stdout.decode('utf-8').strip()
            await message.answer(f"⚠️ Speedtest failed.\nError: {error_msg}")
            return
            
        data = json.loads(stdout.decode('utf-8'))
    except FileNotFoundError:
        await message.answer("⚠️ Official Ookla 'speedtest' CLI is not installed on the system.")
        return
    except Exception as e:
        await message.answer(f"⚠️ Error parsing Speedtest CLI output: {e}")
        return

    # Ookla CLI outputs bandwidth in Bytes per second.
    download = data['download']['bandwidth'] / 125_000
    upload = data['upload']['bandwidth'] / 125_000
    ping = data['ping']['latency']
    timestamp = datetime.utcnow().isoformat()

    save_result(download, upload, ping, timestamp)

    # Safely map variables for the exact required output structure
    server_data = data.get('server', {})
    interface_data = data.get('interface', {})
    
    server = {
        'name': server_data.get('name', 'Unknown'),
        'country': server_data.get('location', 'Unknown'),
        'cc': server_data.get('country', 'N/A'),
        'sponsor': server_data.get('host', 'Ookla'),
        'latency': ping,
        'lat': 'N/A', 
        'lon': 'N/A'
    }
    
    # Fetch geolocation data dynamically
    raw_ip = interface_data.get('externalIp', '0.0.0.0')
    geo_data = await fetch_ip_geo(raw_ip)

    client = {
        'ip': raw_ip,
        'lat': geo_data.get('lat', 'N/A'),
        'lon': geo_data.get('lon', 'N/A'),
        'country': geo_data.get('country', data.get('country', 'N/A')),
        'city': geo_data.get('city', 'Unknown'),
        'region': geo_data.get('regionName', 'Unknown'),
        'isp': geo_data.get('isp', data.get('isp', 'Unknown')),
        'asn': geo_data.get('as', 'Unknown'),
        'org': geo_data.get('org', 'Unknown')
    }

    masked_ip = mask_ip(client['ip'])
    uptime = get_uptime()

    # Convert total bytes to Megabytes for the caption
    bytes_sent = data['upload']['bytes'] / 1_000_000
    bytes_received = data['download']['bytes'] / 1_000_000

    caption = (
        f"<b>🚀 SPEEDTEST INFO 🚀</b>\n"
        f"├ Upload: {upload:.2f} MB/s\n"
        f"├ Download: {download:.2f} MB/s\n"
        f"├ Ping: {ping:.3f} ms\n"
        f"├ Time:\n{timestamp}\n"
        f"├ VPS Uptime: {uptime}\n"
        f"├ Data Sent: {bytes_sent:.2f}MB\n"
        f"├ Data Received: {bytes_received:.2f}MB\n\n"
        f"<b>🌐 SPEEDTEST SERVER 🌐</b>\n"
        f"├ Name: {server['name']}\n"
        f"├ Country: {server['country']}, {server['cc']}\n"
        f"├ Sponsor: {server['sponsor']}\n"
        f"├ Latency: {server['latency']:.3f} ms\n"
        f"├ Latitude: {server['lat']}\n"
        f"├ Longitude: {server['lon']}\n\n"
        f"<b>👤 CLIENT DETAILS 👤</b>\n"
        f"├ IP Address: {masked_ip}\n"
        f"├ Location: {client['city']}, {client['region']}, {client['country']}\n"
        f"├ Coordinates: {client['lat']}, {client['lon']}\n"
        f"├ ISP: {client['isp']}\n"
        f"├ ASN: {client['asn']}\n"
        f"├ Organization: {client['org']}\n\n"
        f'<b>🛸 Powered by <a href="https://github.com/yuIlariy/speedo">Speedo</a> 🪆</b>'
    )

    await message.answer_photo(photo=THUMBNAIL_URL, caption=caption)


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


@router.message(Command("monthlytrend"))
async def monthlytrend_handler(message: Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("🚫 Admin only.")
        return

    now = datetime.utcnow()
    try:
        with open(RESULTS_LOG) as f:
            data = json.load(f)

        month_data = [
            d for d in data
            if datetime.fromisoformat(d["timestamp"]).month == now.month
            and datetime.fromisoformat(d["timestamp"]).year == now.year
        ]

        if not month_data:
            await message.answer("📭 No tests found for this month.")
            return

        timestamps = [datetime.fromisoformat(d["timestamp"]) for d in month_data]
        downloads = [d["download"] for d in month_data]
        uploads = [d["upload"] for d in month_data]

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

        path = "results/speedplot_monthly.png"
        plt.savefig(path)
        await message.answer_photo(
            photo=FSInputFile(path),
            caption=random.choice(captions.get(trend, captions["unknown"]))
        )
    except Exception as e:
        await message.answer(f"⚠️ Error plotting monthly trend\n{e}")


@router.message(Command("trend"))
async def trend_handler(message: Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("🚫 Admin only.")
        return

    try:
        with open(RESULTS_LOG) as f:
            data = json.load(f)
        recent = data[-30:]

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

        captions = {
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
            ]
        }

        await message.answer_photo(
            photo=FSInputFile(path),
            caption=random.choice(captions.get(summary, captions["unknown"]))
        )
    except Exception as e:
        await message.answer(f"⚠️ No results found to plot.\n{e}")
