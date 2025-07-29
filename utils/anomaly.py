import asyncio
from config import ADMIN_ID
from utils.sysmetrics import get_sys_metrics
from aiogram import Bot

THRESHOLDS = {
    "cpu": 90,
    "ram": 90,
    "disk": 90,
    "loadavg": 90
}

ANOMALY_TASK = None
ANOMALY_ACTIVE = False
LAST_ALERT = {}

async def run_anomaly_watch(bot: Bot):
    global LAST_ALERT, ANOMALY_ACTIVE
    ANOMALY_ACTIVE = True

    while ANOMALY_ACTIVE:
        metrics = get_sys_metrics()

        for key, threshold in THRESHOLDS.items():
            val = metrics.get(key, 0)
            if key == "loadavg":
                val = metrics["load"][0] * 25  # Normalize

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
                    pass  # Ignore transient failure

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


  
