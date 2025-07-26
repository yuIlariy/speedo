from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import FSInputFile, Message
from config import ADMIN_ID
from utils.telemetry import generate_syschart
from tempfile import NamedTemporaryFile

router = Router()

@router.message(Command("syschart"))
async def handle_syschart(message: Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("🚫 Admin only.")
        return

    await message.answer("🧮 Generating system snapshot, please hold…")
    image_bytes = await generate_syschart()

    with NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        tmp.write(image_bytes.read())
        tmp.flush()
        input_photo = FSInputFile(tmp.name)
        await message.answer_photo(photo=input_photo)

