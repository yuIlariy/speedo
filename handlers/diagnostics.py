from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.filters.command import CommandObject
import subprocess

from config import ADMIN_ID
from utils.ping_targets import get_ping_targets

router = Router()

@router.message(Command("pingtest"))
async def pingtest_handler(message: Message, command: CommandObject):
    if message.from_user.id != ADMIN_ID:
        await message.answer("🚫 Admin only.")
        return

    input_arg = command.args.strip() if command.args else None

    if input_arg:
        targets = {input_arg: input_arg}
        intro = f"📡 Target specified: <code>{input_arg}</code>. Pinging…"
    else:
        targets = get_ping_targets()
        intro = "🏓 Launching packets toward default targets…"

    await message.answer(intro)

    results = []
    for name, ip in targets.items():
        try:
            output = subprocess.check_output(f"ping -c 5 {ip}", shell=True).decode()
            loss_line = [line for line in output.splitlines() if "packet loss" in line]
            latency_line = [line for line in output.splitlines() if "min/avg/max" in line]

            loss = loss_line[0].strip() if loss_line else "N/A"
            latency = latency_line[0].strip() if latency_line else "N/A"
            verdict = "🔥 Stable" if "0% packet loss" in loss else (
                "⚠️ Okay" if "1%" in loss or "2%" in loss else "❌ Poor"
            )

            results.append(f"<b>{name}</b>\n{verdict}\n📡 {loss}\n📶 {latency}\n")
        except Exception as e:
            results.append(f"<b>{name}</b>\n❌ Error: {e}\n")

    await message.answer("<b>🧪 Ping Test Results</b>\n\n" + "\n".join(results))



