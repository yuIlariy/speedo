import asyncio
import os
import json
import shutil
from datetime import datetime
from aiogram import Bot
from config import ADMIN_ID
from utils.helpers import get_uptime, save_result

STATE_PATH = "speedo_storage/autospeed_state.json"

AUTO_LAST_RUN = None
INTERVAL = 3600  # 👈 1 Hour

def save_autospeed_state():
    data = {
        "last_run": AUTO_LAST_RUN.isoformat() if AUTO_LAST_RUN else None
    }
    os.makedirs(os.path.dirname(STATE_PATH), exist_ok=True)
    try:
        with open(STATE_PATH, "w") as f:
            json.dump(data, f)
    except Exception:
        pass

async def perform_speedtest(bot: Bot):
    global AUTO_LAST_RUN
    
    binary_path = shutil.which('speedtest')
    if not binary_path:
        print("🚨 Auto-speedtest error: 'speedtest' binary not found in system PATH.")
        return

    process = None
    try:
        # Run official Ookla speedtest CLI asynchronously
        process = await asyncio.create_subprocess_exec(
            binary_path, '--accept-license', '--accept-gdpr', '-f', 'json',
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        # Enforce a strict 3-minute timeout to handle deadlocks or hung routes gracefully
        stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=180.0)
        
        if process.returncode != 0:
            print(f"Auto-speedtest failed: {stderr.decode('utf-8').strip() or stdout.decode('utf-8').strip()}")
            return
            
        data = json.loads(stdout.decode('utf-8'))
        
        # Convert Ookla's bytes/second to Mbps
        download = data['download']['bandwidth'] / 125_000
        upload = data['upload']['bandwidth'] / 125_000
        ping = data['ping']['latency']
        
        AUTO_LAST_RUN = datetime.utcnow()
        save_result(download, upload, ping, AUTO_LAST_RUN.isoformat())

        caption = (
            f"⏰ <b>Speedo Auto Speedtest</b>\n"
            f"🕒 <b>Time:</b> {AUTO_LAST_RUN.isoformat()}\n"
            f"⬇️ <b>Download:</b> {download:.2f} Mbps\n"
            f"⬆️ <b>Upload:</b> {upload:.2f} Mbps\n"
            f"📶 <b>Ping:</b> {ping:.2f} ms\n"
            f"🖥 <b>VPS Uptime:</b> {get_uptime()}"
        )
        await bot.send_message(ADMIN_ID, caption)
        print("✅ Auto-speedtest executed successfully.")
    except asyncio.TimeoutError:
        print("🚨 Auto-speedtest timed out! The process took too long.")
        if process:
            try: process.kill()
            except Exception: pass
    except Exception as e:
        print(f"Auto-speedtest error: {e}")
    finally:
        save_autospeed_state()

async def start_autospeed_monitor(bot: Bot):
    print("⏳ Auto-speedtest monitor initialization loop started.")
    while True:
        try:
            await perform_speedtest(bot)
        except Exception as e:
            print(f"🚨 Critical exception inside monitor loop structure: {e}")
            
        # 💤 Sleep explicitly for 1 hour before attempting next cycle
        await asyncio.sleep(INTERVAL)
