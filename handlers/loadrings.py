from aiogram import Router
from aiogram.types import Message, BufferedInputFile
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
        img_buf, theme_caption = render_rings_random()
        flair = random.choice(CAPTIONS)
        final_caption = f"{flair}\n🎨 Theme: {theme_caption}"

        image = BufferedInputFile(img_buf, filename="loadrings.png")
        await msg.answer_photo(photo=image, caption=final_caption)
    except Exception as e:
        error_text = f"⚠️ Failed to render /loadrings.\nError: {type(e).__name__}: {str(e)}"
        await msg.answer(error_text, parse_mode=None)


