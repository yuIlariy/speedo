from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from config import ADMIN_ID
from speedo_core.monitor import toggle_autospeed, get_autospeed_status

router = Router()

@router.message(Command("autospeed"))
async def cmd_autospeed(msg: Message):
    if msg.from_user.id != ADMIN_ID:
        return

    text = msg.text.lower().strip().split()
    args = [arg for arg in text if arg != "/autospeed"]

    if "on" in args:
        # Extract duration argument like '3m', '1h', etc.
        duration = next((arg for arg in args if arg != "on"), "1h")
        await toggle_autospeed(msg.bot, True, duration)
        await msg.answer(f"📡 AutoSpeed enabled every {duration} ✅")
    elif "off" in args:
        await toggle_autospeed(msg.bot, False)
        await msg.answer("🛑 AutoSpeed disabled.")
    else:
        await msg.answer(
            "🧭 Usage:\n"
            "/autospeed on 2h → every 2 hours\n"
            "/autospeed on 30m → every 30 minutes\n"
            "/autospeed on 45s → every 45 seconds\n"
            "/autospeed off → stop monitor"
        )

@router.message(Command("autospeedstatus"))
async def cmd_autospeedstatus(msg: Message):
    if msg.from_user.id != ADMIN_ID:
        return
    await msg.answer(get_autospeed_status(), parse_mode="HTML")


