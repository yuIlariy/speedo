from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import ADMIN_ID
from utils.processwatch import top_processes, format_process_panel
import psutil  # ✅ Added for system-wide stats

router = Router()

def get_system_usage():
    cpu = psutil.cpu_percent(interval=None)
    ram = psutil.virtual_memory().percent
    return cpu, ram

def build_panel():
    procs = top_processes()
    panel = "**🕸 Process Watch Panel**\n🚀 = CPU • 💾 = RAM\n\n"
    panel += format_process_panel(procs)

    # ✅ Add total system usage at the bottom
    cpu_total, ram_total = get_system_usage()
    mood = "🌋 Overloaded" if cpu_total > 80 or ram_total > 85 else \
           "🌡 Moderate" if cpu_total > 50 or ram_total > 60 else "❄️ Chill"
    panel += f"\n\n🌌 **Total Usage** — 🚀 {cpu_total:.1f}% • 💾 {ram_total:.1f}% • {mood}"
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

