from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from utils.anomaly import toggle_anomaly

router = Router()

@router.message(Command("anomalywatch"))
async def cmd_anomalywatch(msg: Message):
    cmd = msg.text.lower()

    if "on" in cmd:
        await toggle_anomaly(msg.bot, state=True)
        await msg.answer("🧠 AnomalyWatch activated • monitoring spikes...")
    elif "off" in cmd:
        await toggle_anomaly(msg.bot, state=False)
        await msg.answer("🛑 AnomalyWatch disabled.")
    else:
        await msg.answer("🧭 Usage:\n/anomalywatch on → start monitor\n/anomalywatch off → stop monitor")

  
