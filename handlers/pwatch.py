from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import ADMIN_ID
from utils.processwatch import top_processes, format_process_panel

router = Router()

@router.message(Command("pwatch"))
async def pwatch_handler(message: Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("🚫 Admin only.")
        return

    procs = top_processes()
    panel = "**🕸 Process Watch Panel**\n🚀 = CPU • 💾 = RAM\n\n" + format_process_panel(procs)

    kb = InlineKeyboardBuilder()
    kb.button(text="🔄 Refresh", callback_data="refresh_pwatch")
    await message.answer(panel, reply_markup=kb.as_markup(), parse_mode="Markdown")

@router.callback_query(lambda c: c.data == "refresh_pwatch")
async def pwatch_refresh(query: CallbackQuery):
    procs = top_processes()
    panel = "**🕸 Process Watch Panel**\n🚀 = CPU • 💾 = RAM\n\n" + format_process_panel(procs)

    kb = InlineKeyboardBuilder()
    kb.button(text="🔄 Refresh", callback_data="refresh_pwatch")
    await query.message.edit_text(panel, reply_markup=kb.as_markup(), parse_mode="Markdown")
    await query.answer("🔁 Process panel refreshed.")


