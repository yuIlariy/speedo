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

    parts = msg.text.split()
    if "on" in msg.text.lower():
        try:
            hours = int(parts[-1])
        except:
            hours = 1
        await toggle_autospeed(msg.bot, True, hours)
        await msg.answer(f"📡 AutoSpeed enabled every {hours}h ✅")
    elif "off" in msg.text.lower():
        await toggle_autospeed(msg.bot, False)
        await msg.answer("🛑 AutoSpeed disabled.")
    else:
        await msg.answer("🧭 Usage:\n/autospeed on 2 → start every 2h\n/autospeed off → stop monitor")

@router.message(Command("autospeedstatus"))
async def cmd_autospeedstatus(msg: Message):
    if msg.from_user.id != ADMIN_ID:
        return
    await msg.answer(get_autospeed_status(), parse_mode="HTML")


