from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from utils.loadrings import render_rings_random
import random

router = Router()

# ─── Caption Variants ────────────────────────────────────
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
    try:
        image = render_rings_random()
        flair = random.choice(CAPTIONS)
        await msg.answer_photo(photo=image, caption=flair)
    except Exception as e:
        await msg.answer(f"⚠️ Error generating /loadrings: {type(e).__name__}\n{str(e)}")

