from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from utils.loadrings import render_rings_random

router = Router()

# ─── Caption Variants ────────────────────────────────────
CAPTIONS = [
    "🧠 VPS Orbit • Rings spinning stable",
    "🪐 Loadrings Sync • All sectors green",
    "🌈 Gauge Parade • No pressure spikes",
    "🚀 Core Systems Check • Nominal across all rings",
    "🌌 Status Halo • Loadrings lit & balanced",
]

@router.message(Command("loadrings"))
async def handle_loadrings(msg: Message):
    image, theme_caption = render_rings_random()
    flair = random.choice(CAPTIONS)

    final_caption = f"{flair}\n🎨 Theme: {theme_caption}"
    await msg.answer_photo(photo=image, caption=final_caption)

