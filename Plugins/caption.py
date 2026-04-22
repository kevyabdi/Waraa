import logging
from pyrogram import Client, filters
from pyrogram.types import Message

from script import Script
from Helper.database import set_caption, get_caption, del_caption
from Helper.utils import maintenance_check

logger = logging.getLogger("waraa.caption")

# ════════════════════════════════════════════
#       WARAA BOT — CAPTION HANDLER
# ════════════════════════════════════════════

_awaiting_caption: set[int] = set()


@Client.on_message(filters.command("set_caption") & filters.private)
@maintenance_check
async def ask_caption(client: Client, message: Message):
    _awaiting_caption.add(message.from_user.id)
    await message.reply(Script.CAPTION_TXT + "\n\n✏️ **Hadda caption-kaaga qor:**")


@Client.on_message(filters.command("see_caption") & filters.private)
async def view_caption(client: Client, message: Message):
    cap = await get_caption(message.from_user.id)
    if cap:
        await message.reply(f"📝 **Caption-kaaga:**\n\n`{cap}`")
    else:
        await message.reply("❌ **Caption ma dejisan.** Isticmaal /set_caption.")


@Client.on_message(filters.command("del_caption") & filters.private)
async def delete_caption(client: Client, message: Message):
    await del_caption(message.from_user.id)
    await message.reply("🗑️ **Caption-kaaga waa la tirtiray.**")


@Client.on_message(filters.private & filters.text)
async def caption_input(client: Client, message: Message):
    user_id = message.from_user.id
    if user_id not in _awaiting_caption:
        return
    _awaiting_caption.discard(user_id)
    await set_caption(user_id, message.text.strip())
    await message.reply(f"✅ **Caption waa la keydiay:**\n\n`{message.text.strip()}`")