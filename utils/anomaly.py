import asyncio
from config import ADMIN_ID
from aiogram import Bot
import psutil

THRESHOLDS = {
    "cpu": 10,
    "ram": 10,
    "disk": 10,
    "loadavg": 10
}

ANOMALY_TASK = None
ANOMALY_ACTIVE = False
LAST_ALERT = {}

# 🧠 Metric Collector (Fallback Logic)
def get_sys_metrics():
    return {
        "cpu": psutil.cpu_percent(interval=None),
        "ram": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage("/").percent,
        "load": psutil.getloadavg()  # Tuple (1m, 5m, 15m)
    }

async def run_anomaly_watch(bot: Bot):
    global LAST_ALERT, ANOMALY_ACTIVE
    ANOMALY_ACTIVE = True

    while ANOMALY_ACTIVE:
        metrics = get_sys_metrics()

        for key, threshold in THRESHOLDS.items():
            val = metrics.get(key, 0)
            if key == "loadavg":
                val = metrics["load"][0] * 25  # Normalize for %
            if val >= threshold and LAST_ALERT.get(key) != val:
                LAST_ALERT[key] = val
                alert = (
                    f"🚨 <b>System Spike Detected</b>\n"
                    f"📊 <b>{key.upper()}:</b> {val:.1f}%\n"
                    f"⚠️ <b>Threshold:</b> {threshold}%"
                )
                try:
                    await bot.send_message(ADMIN_ID, alert, parse_mode="HTML")
                except:
                    pass

        await asyncio.sleep(10)

async def toggle_anomaly(bot: Bot, state: bool):
    global ANOMALY_TASK, ANOMALY_ACTIVE
    if state and not ANOMALY_ACTIVE:
        ANOMALY_TASK = asyncio.create_task(run_anomaly_watch(bot))
    elif not state and ANOMALY_ACTIVE:
        ANOMALY_ACTIVE = False
        if ANOMALY_TASK:
            ANOMALY_TASK.cancel()
            ANOMALY_TASK = None


