from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from config import ADMIN_ID
from utils.network import get_network_panel

router = Router()

@router.message(Command("netstatus"))
async def netstatus_handler(message: Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("🚫 Admin only.")
        return

    await message.answer("📡 Gathering interface stats…")
    panel = get_network_panel()
    await message.answer(panel, parse_mode="Markdown")

