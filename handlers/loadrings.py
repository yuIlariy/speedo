from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from utils.loadrings import render_rings, get_sys_metrics

import random

router = Router()

# ─── Random Caption Variants ─────────────────────────────
CAPTIONS = [
    "🧠 VPS Orbit • Rings spinning stable",
    "🪐 Loadrings Sync • All sectors green",
    "🌈 Gauge Parade • No pressure spikes",
    "🚀 Core Systems Check • Nominal across all rings",
    "🌌 Status Halo • Loadrings lit & balanced",
]

# ─── Main Handler ────────────────────────────────────────
@router.message(Command("loadrings"))
async def handle_loadrings(msg: Message):
    metrics = get_sys_metrics()
    theme = "dark"  # You can swap this with a DB/user config later

    image = render_rings(theme=theme, metrics=metrics)
    caption = random.choice(CAPTIONS)

    await msg.answer_photo(photo=image, caption=caption)


