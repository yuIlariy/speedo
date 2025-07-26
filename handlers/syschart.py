from aiogram import Router, types
from aiogram.filters import Command
from config import ADMIN_ID
from utils.telemetry import generate_syschart

router = Router()

@router.message(Command("syschart"))
async def handle_syschart(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("🚫 Admin only.")
        return

    await message.answer("🧮 Generating system snapshot, please hold…")
    image_bytes = await generate_syschart()
    await message.answer_photo(photo=image_bytes)

