from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import ADMIN_ID
from utils.processwatch import top_processes, format_process_panel
import psutil

router = Router()

def build_panel():
    procs = top_processes()
    panel = "**🕸 Process Watch Panel**\n🚀 = CPU • 💾 = RAM\n\n"
    panel += format_process_panel(procs)

    # ✅ Sum actual usage from normalized values
    cpu_sum = sum(p[3] for p in procs)  # p[3] = CPU %
    ram_sum = sum(p[2] for p in procs)  # p[2] = RAM %

    mood = "🌋 Overloaded" if cpu_sum > 80 or ram_sum > 85 else \
           "🌡 Moderate" if cpu_sum > 50 or ram_sum > 60 else "❄️ Chill"

    panel += f"\n\n🌌 **Panel Total** — 🚀 {cpu_sum:.1f}% • 💾 {ram_sum:.1f}% • {mood}"
    return panel

@router.message(Command("pwatch"))
async def pwatch_handler(message: Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("🚫 Admin only.")
        return

    panel = build_panel()
    kb = InlineKeyboardBuilder()
    kb.button(text="🔄 Refresh", callback_data="refresh_pwatch")
    await message.answer(panel, reply_markup=kb.as_markup(), parse_mode="Markdown")

@router.callback_query(lambda c: c.data == "refresh_pwatch")
async def pwatch_refresh(query: CallbackQuery):
    panel = build_panel()
    kb = InlineKeyboardBuilder()
    kb.button(text="🔄 Refresh", callback_data="refresh_pwatch")
    await query.message.edit_text(panel, reply_markup=kb.as_markup(), parse_mode="Markdown")
    await query.answer("🔁 Process panel refreshed.")


