from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.filters.command import CommandObject

router = Router()

import os
from aiogram.types.input_file import FSInputFile
from config import ADMIN_ID, RESULTS_LOG

@router.message(Command("exportlog"))
async def exportlog_handler(message: Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("🚫 Admin only.")
        return

    if not os.path.exists(RESULTS_LOG):
        await message.answer("📭 Log file is missing.")
        return

    document = FSInputFile(RESULTS_LOG)
    await message.answer_document(document, caption="🧾 Log dump: speedlog.json")


