from aiogram import Router, types, Bot
from utils.authwatch import parse_auth_log
from config import ADMIN_ID

router = Router()
AUTHWATCH_ACTIVE = False

def is_admin(user_id: int) -> bool:
    return user_id == ADMIN_ID

@router.message(commands=["authwatch"])
async def toggle_authwatch(msg: types.Message):
    if not is_admin(msg.from_user.id):
        return await msg.reply("⛔ Unauthorized access.")
    
    global AUTHWATCH_ACTIVE
    AUTHWATCH_ACTIVE = not AUTHWATCH_ACTIVE
    status = "🟢 Active" if AUTHWATCH_ACTIVE else "⚪ Inactive"
    await msg.reply(f"Authwatch toggled: {status}")
    alert = "🔔 Activated." if AUTHWATCH_ACTIVE else "🔕 Deactivated."
    await msg.bot.send_message(ADMIN_ID, f"Authwatch: {alert}")

@router.message(commands=["authwatchs"])
async def check_authwatch_status(msg: types.Message):
    if not is_admin(msg.from_user.id):
        return await msg.reply("⛔ Unauthorized access.")
    
    status = "🟢 Active" if AUTHWATCH_ACTIVE else "⚪ Inactive"
    await msg.reply(f"Authwatch status: {status}")

@router.message(commands=["authstats"])
async def send_authwatch_stats(msg: types.Message):
    if not is_admin(msg.from_user.id):
        return await msg.reply("⛔ Unauthorized access.")

    entries = parse_auth_log()
    success = [e for e in entries if e["status"] == "success"]
    failed = [e for e in entries if e["status"] == "failed"]

    summary = f"📜 Auth Summary\n✅ Success: {len(success)}\n❌ Failed: {len(failed)}\n"
    for e in entries[-5:]:
        summary += f"\n{e['emoji']} {e['caption']}"

    await msg.reply(summary)
    await msg.bot.send_message(chat_id=ADMIN_ID, text=summary)


