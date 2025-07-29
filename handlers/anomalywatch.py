from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from utils.anomaly import toggle_anomaly
from utils.anomaly import manual_report
from utils.anomaly import get_status_report
from utils.anomaly import reset_anomaly_state

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




@router.message(Command("anomalyreport"))
async def cmd_anomalyreport(msg: Message):
    await manual_report(msg.bot)



@router.message(Command("anomalystatus"))
async def cmd_anomalystatus(msg: Message):
    status = get_status_report()
    await msg.answer(status)



def register_reset_handler(dp: Dispatcher, bot: Bot):
    @dp.message_handler(commands=["resetanomaly"])
    async def handle_reset(message: types.Message):
        reset_anomaly_state()
        await bot.send_message(
            message.chat.id,
            "🧹 <b>Anomaly system reset</b>\nAll spike logs and alert history wiped."
        )
