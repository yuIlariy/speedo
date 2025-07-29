import asyncio
from config import ADMIN_ID
from aiogram import Bot
import psutil
from datetime import datetime

ANOMALY_TASK = None
REPORT_TASK = None
ANOMALY_ACTIVE = False
LAST_ALERT = {}
SPIKE_LOG = {}
THRESHOLD_LEVEL = 90  # default

METRICS = {
    "cpu": lambda: psutil.cpu_percent(interval=None),
    "ram": lambda: psutil.virtual_memory().percent,
    "disk": lambda: psutil.disk_usage("/").percent,
    "loadavg": lambda: psutil.getloadavg()[0] * 25  # normalize
}

async def run_anomaly_watch(bot: Bot):
    global LAST_ALERT, ANOMALY_ACTIVE, SPIKE_LOG
    ANOMALY_ACTIVE = True

    while ANOMALY_ACTIVE:
        for key, getter in METRICS.items():
            val = getter()
            if val >= THRESHOLD_LEVEL and LAST_ALERT.get(key) != val:
                LAST_ALERT[key] = val
                now = datetime.utcnow().strftime("%H:%M")
                SPIKE_LOG.setdefault(key, []).append((val, now))
                alert = (
                    f"🚨 <b>System Spike Detected</b>\n"
                    f"📊 <b>{key.upper()}:</b> {val:.1f}%\n"
                    f"⏱ <b>Time:</b> {now} UTC\n"
                    f"⚠️ <b>Threshold:</b> {THRESHOLD_LEVEL}%"
                )
                try:
                    await bot.send_message(ADMIN_ID, alert, parse_mode="HTML")
                except:
                    pass
        await asyncio.sleep(10)

async def auto_report(bot: Bot):
    global SPIKE_LOG
    while ANOMALY_ACTIVE:
        await asyncio.sleep(43200)  # 12h

        if not SPIKE_LOG:
            caption = "✅ <b>Anomaly Summary</b>\nNo spikes detected in the last 12 hours."
        else:
            parts = [f"📈 <b>{k.upper()}:</b> {len(v)}× spikes"]
            for k, v in SPIKE_LOG.items():
                spikes = ", ".join(f"{val:.1f}%@{t}" for val, t in v)
                parts.append(f"• {k}: {spikes}")
            caption = "<b>📊 12h Anomaly Summary</b>\n" + "\n".join(parts)

        try:
            await bot.send_message(ADMIN_ID, caption, parse_mode="HTML")
        except:
            pass

        SPIKE_LOG = {}

async def toggle_anomaly(bot: Bot, state: bool, threshold: int = 90):
    global ANOMALY_TASK, REPORT_TASK, ANOMALY_ACTIVE, THRESHOLD_LEVEL
    THRESHOLD_LEVEL = threshold

    if state and not ANOMALY_ACTIVE:
        ANOMALY_ACTIVE = True
        ANOMALY_TASK = asyncio.create_task(run_anomaly_watch(bot))
        REPORT_TASK = asyncio.create_task(auto_report(bot))
    elif not state and ANOMALY_ACTIVE:
        ANOMALY_ACTIVE = False
        if ANOMALY_TASK:
            ANOMALY_TASK.cancel()
        if REPORT_TASK:
            REPORT_TASK.cancel()
        ANOMALY_TASK = None
        REPORT_TASK = None

async def manual_report(bot: Bot):
    global SPIKE_LOG
    if not SPIKE_LOG:
        caption = "📊 <b>Manual Anomaly Report</b>\nNo recent anomalies tracked."
    else:
        parts = [f"📊 <b>Manual Anomaly Report</b>"]
        for k, v in SPIKE_LOG.items():
            spikes = ", ".join(f"{val:.1f}%@{t}" for val, t in v)
            parts.append(f"• <b>{k.upper()}:</b> {len(v)}× → {spikes}")
        caption = "\n".join(parts)

    try:
        await bot.send_message(ADMIN_ID, caption, parse_mode="HTML")
    except:
        pass

def get_status_report() -> str:
    global ANOMALY_ACTIVE, THRESHOLD_LEVEL, LAST_ALERT, SPIKE_LOG

    status = "🧭 <b>Anomaly Status</b>\n"
    status += f"🔌 <b>Monitor:</b> {'Active ✅' if ANOMALY_ACTIVE else 'Inactive ❌'}\n"
    status += f"🎚️ <b>Threshold:</b> {THRESHOLD_LEVEL}%\n"

    if LAST_ALERT:
        status += "📊 <b>Last Alerts:</b>\n"
        for k, v in LAST_ALERT.items():
            status += f"• {k.upper()}: {v:.1f}%\n"
    else:
        status += "📊 <b>Last Alerts:</b> None"

    if SPIKE_LOG:
        total = sum(len(v) for v in SPIKE_LOG.values())
        status += f"\n📈 <b>Tracked Spikes:</b> {total} event(s)"
    else:
        status += "\n📈 <b>Tracked Spikes:</b> None"

    return status

def reset_anomaly_state():
    global ANOMALY_ACTIVE, LAST_ALERT, SPIKE_LOG, ANOMALY_TASK, REPORT_TASK
    ANOMALY_ACTIVE = False
    LAST_ALERT.clear()
    SPIKE_LOG.clear()
    if ANOMALY_TASK:
        ANOMALY_TASK.cancel()
        ANOMALY_TASK = None
    if REPORT_TASK:
        REPORT_TASK.cancel()
        REPORT_TASK = None

