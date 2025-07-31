from aiogram import Router, types
from utils.authwatch import parse_auth_log

router = Router()
AUTHWATCH_ACTIVE = False

@router.message(commands=["authwatch"])
async def toggle_authwatch(msg: types.Message):
    global AUTHWATCH_ACTIVE
    AUTHWATCH_ACTIVE = not AUTHWATCH_ACTIVE
    status = "🟢 Active" if AUTHWATCH_ACTIVE else "⚪ Inactive"
    await msg.reply(f"Authwatch toggled: {status}")

@router.message(commands=["authwatchs"])
async def check_authwatch_status(msg: types.Message):
    status = "🟢 Active" if AUTHWATCH_ACTIVE else "⚪ Inactive"
    await msg.reply(f"Authwatch status: {status}")

@router.message(commands=["authstats"])
async def send_authwatch_stats(msg: types.Message):
    entries = parse_auth_log()
    success = [e for e in entries if e["status"] == "success"]
    failed = [e for e in entries if e["status"] == "failed"]

    summary = f"📜 Auth Summary\n✅ Success: {len(success)}\n❌ Failed: {len(failed)}\n"
    for e in entries[-5:]:
        summary += f"\n{e['emoji']} {e['caption']}"
    await msg.reply(summary)


