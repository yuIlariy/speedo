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
    if "on" in text:
        # Extract duration string if present, default to 1h
        try:
            duration = next((t for t in text if t != "on"), "1h")
        except:
            duration = "1h"

        await toggle_autospeed(msg.bot, True, duration)
        await msg.answer(f"📡 AutoSpeed enabled every {duration} ✅")
    elif "off" in text:
        await toggle_autospeed(msg.bot, False)
        await msg.answer("🛑 AutoSpeed disabled.")
    else:
        await msg.answer(
            "🧭 Usage:\n"
            "/autospeed on 2h → every 2 hours\n"
            "/autospeed on 30m → every 30 minutes\n"
            "/autospeed off → stop monitor"
        )

@router.message(Command("autospeedstatus"))
async def cmd_autospeedstatus(msg: Message):
    if msg.from_user.id != ADMIN_ID:
        return
    await msg.answer(get_autospeed_status(), parse_mode="HTML")

