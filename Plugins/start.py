import logging
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from script import Script
from config import START_PIC, FORCE_SUBS, ADMIN
from Helper.database import add_user, get_user_count, is_premium

logger = logging.getLogger("waraa.start")

# ════════════════════════════════════════════
#       WARAA BOT — START & CORE COMMANDS
# ════════════════════════════════════════════

START_BUTTONS = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("📖 Caawimo",    callback_data="help"),
        InlineKeyboardButton("ℹ️ Ku saabsan", callback_data="about"),
    ],
    [
        InlineKeyboardButton("💎 Premium",    callback_data="premium"),
        InlineKeyboardButton("📊 Xogahaaga",  callback_data="stats"),
    ],
    [
        InlineKeyboardButton("🔔 Channel", url="https://t.me/your_channel"),
    ],
])

BACK_BUTTON = InlineKeyboardMarkup([
    [InlineKeyboardButton("🔙 Dib u noqo", callback_data="start")]
])


async def _check_force_sub(client: Client, user_id: int) -> bool:
    if not FORCE_SUBS:
        return True
    try:
        member = await client.get_chat_member(f"@{FORCE_SUBS}", user_id)
        return member.status.value not in ("left", "kicked")
    except Exception:
        return True


@Client.on_message(filters.command("start") & filters.private)
async def start_handler(client: Client, message: Message):
    user = message.from_user
    await add_user(user.id)

    if not await _check_force_sub(client, user.id):
        await message.reply(
            Script.FORCE_SUB_TXT.format(f"https://t.me/{FORCE_SUBS}"),
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🔔 Biir", url=f"https://t.me/{FORCE_SUBS}")
            ]])
        )
        return

    name = user.first_name or "Saaxiib"
    text = Script.START_TXT.format(name)

    if START_PIC:
        await message.reply_photo(START_PIC, caption=text, reply_markup=START_BUTTONS)
    else:
        await message.reply(text, reply_markup=START_BUTTONS)

    logger.info("/start from user %d (@%s)", user.id, user.username or "none")


@Client.on_message(filters.command("ping") & filters.private)
async def ping_handler(client: Client, message: Message):
    import time
    start = time.perf_counter()
    msg   = await message.reply("🏓 Pinging...")
    ms    = (time.perf_counter() - start) * 1000
    await msg.edit(f"🏓 **Pong!** `{ms:.2f} ms`")


@Client.on_message(filters.command("stats") & filters.private)
async def stats_handler(client: Client, message: Message):
    from Helper.database import get_user_stats
    data = await get_user_stats(message.from_user.id)
    joined = data["joined_date"]
    if hasattr(joined, "strftime"):
        joined = joined.strftime("%Y-%m-%d")
    await message.reply(Script.STATS_TXT.format(**{**data, "joined_date": joined}))


@Client.on_message(filters.command("myplan") & filters.private)
async def plan_handler(client: Client, message: Message):
    from Helper.database import get_premium
    user_id = message.from_user.id
    doc     = await get_premium(user_id)

    if doc and doc.get("active"):
        expires = doc["expires"].strftime("%Y-%m-%d") if doc.get("expires") else "♾️ Weligiis"
        limit   = "4 GB" if doc["plan"] == "premium" else "2 GB"
        await message.reply(
            Script.PLAN_TXT.format(user_id, doc["plan"].upper(), limit, expires)
        )
    else:
        await message.reply(
            Script.PLAN_TXT.format(user_id, "FREE", "2 GB", "—")
        )