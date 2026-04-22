import os
import time
import asyncio
import logging
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from script import Script
from config import AUTO_DELETE_TIME
from Helper.database import (
    get_thumbnail, get_caption, get_metadata,
    get_auto_delete, increment_rename
)
from Helper.utils import progress_bar, humanbytes, rate_limit, maintenance_check

logger = logging.getLogger("waraa.rename")

# ════════════════════════════════════════════
#       WARAA BOT — RENAME HANDLER
# ════════════════════════════════════════════

# Track pending rename requests: {user_id: message}
_pending: dict[int, Message] = {}


@Client.on_message(
    filters.private
    & (filters.document | filters.video | filters.audio)
)
@maintenance_check
@rate_limit
async def file_received(client: Client, message: Message):
    """Step 1 — user sends a file; ask for new name."""
    user_id = message.from_user.id

    # Get original filename
    media = message.document or message.video or message.audio
    orig  = getattr(media, "file_name", None) or "file"

    _pending[user_id] = message

    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("❌ Jooji", callback_data="cancel_rename")]
    ])

    await message.reply(
        Script.RENAME_TXT.format(orig),
        reply_markup=buttons
    )


@Client.on_message(filters.private & filters.text & ~filters.command(["start","help","ping","stats","myplan"]))
@maintenance_check
async def new_name_received(client: Client, message: Message):
    """Step 2 — user types the new filename."""
    user_id  = message.from_user.id
    orig_msg = _pending.pop(user_id, None)

    if not orig_msg:
        return  # no pending rename for this user

    new_name = message.text.strip()
    if not new_name:
        await message.reply("❌ Magac faaruq ah. Dib u isku day.")
        return

    status = await message.reply(Script.RENAME_WAIT)
    media  = orig_msg.document or orig_msg.video or orig_msg.audio

    # ── Download ──────────────────────────────
    try:
        dl_start = time.time()
        file_path = await orig_msg.download(
            progress=progress_bar,
            progress_args=(status, "⬇️ **Soo dejinaya...**", dl_start)
        )
    except Exception as e:
        logger.exception("Download failed for user %d: %s", user_id, e)
        await status.edit(Script.RENAME_FAILED)
        return

    # ── Rename locally ───────────────────────
    ext      = os.path.splitext(getattr(media, "file_name", "") or "")[1]
    if "." not in new_name:
        new_name += ext

    new_path = os.path.join(os.path.dirname(file_path), new_name)
    os.rename(file_path, new_path)

    # ── Gather extras ────────────────────────
    thumb    = await get_thumbnail(user_id)
    caption  = await get_caption(user_id)
    metadata = await get_metadata(user_id)

    # Format caption placeholders
    if caption:
        size_str = humanbytes(media.file_size or 0)
        caption  = caption.replace("{filename}", new_name)\
                          .replace("{filesize}", size_str)
    else:
        caption = f"📄 `{new_name}`"

    # ── Upload ───────────────────────────────
    try:
        ul_start = time.time()
        sent = await orig_msg.reply_document(
            document   = new_path,
            file_name  = new_name,
            caption    = caption,
            thumb      = thumb,
            progress   = progress_bar,
            progress_args = (status, "⬆️ **Diraya...**", ul_start)
        )
    except Exception as e:
        logger.exception("Upload failed for user %d: %s", user_id, e)
        await status.edit(Script.RENAME_FAILED)
        return
    finally:
        # Always clean up temp file
        try:
            os.remove(new_path)
        except OSError:
            pass

    await status.delete()
    await message.reply(Script.RENAME_DONE.format(new_name))

    # ── Track stats ──────────────────────────
    await increment_rename(user_id, media.file_size or 0)

    # ── Auto-delete (user-level, then global) ─
    delay = await get_auto_delete(user_id) or AUTO_DELETE_TIME
    if delay > 0:
        note = await sent.reply(Script.AUTO_DELETE_TXT.format(delay))
        asyncio.create_task(_auto_delete(sent, note, delay))


async def _auto_delete(file_msg: Message, note_msg: Message, delay: int):
    await asyncio.sleep(delay)
    for m in (file_msg, note_msg):
        try:
            await m.delete()
        except Exception:
            pass