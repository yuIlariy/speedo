from aiogram import Router, types
from aiogram.filters import Command
from utils.telemetry import generate_syschart

router = Router()

@router.message(Command("syschart"))
async def handle_syschart(message: types.Message):
    image_bytes = await generate_syschart()
    await message.answer_photo(photo=image_bytes, caption="📊 System Snapshot with Speedtest")

