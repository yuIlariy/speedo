from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from utils.anomaly import toggle_anomaly

router = Router()

@router.message(Command("anomalywatch"))
async def cmd_anomalywatch(msg: Message):
    cmd = msg.text.lower()
    parts = cmd.split()

    if "on" in cmd:
        try:
            threshold = int(parts[-1])
        except:
            threshold = 90
        await toggle_anomaly(msg.bot, state=True, threshold=threshold)
        await msg.answer(f"🧠 AnomalyWatch activated at {threshold}% • auto summary every 12h")
    elif "off" in cmd:
        await toggle_anomaly(msg.bot, state=False)
        await msg.answer("🛑 AnomalyWatch disabled.")
    else:
        await msg.answer("🧭 Usage:\n/anomalywatch on 80 → start with threshold\n/anomalywatch off → stop monitor")


