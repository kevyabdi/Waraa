import logging
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message

from script import Script
from config import ADMIN
from Helper.database import (
    get_user_count, get_all_user_ids, get_all_users,
    add_premium, remove_premium, ban_user, unban_user
)
from Helper.utils import admin_only

logger = logging.getLogger("waraa.admin")

# ════════════════════════════════════════════
#       WARAA BOT — ADMIN COMMANDS
# ════════════════════════════════════════════

admin_filter = filters.private & filters.user(ADMIN)


@Client.on_message(filters.command("users") & admin_filter)
@admin_only
async def cmd_users(client: Client, message: Message):
    count = await get_user_count()
    await message.reply(f"👥 **Isticmaalayaasha guud ahaan:** `{count}`")


@Client.on_message(filters.command("allids") & admin_filter)
@admin_only
async def cmd_allids(client: Client, message: Message):
    ids   = await get_all_user_ids()
    text  = "\n".join(str(i) for i in ids)
    if len(text) > 4000:
        # Send as file if too long
        with open("/tmp/user_ids.txt", "w") as f:
            f.write(text)
        await message.reply_document("/tmp/user_ids.txt", caption="📋 Dhammaan IDs-yada")
    else:
        await message.reply(f"📋 **IDs-yada isticmaalayaasha:**\n\n`{text}`")


@Client.on_message(filters.command("broadcast") & admin_filter)
@admin_only
async def cmd_broadcast(client: Client, message: Message):
    if not message.reply_to_message:
        await message.reply("↩️ **Fariinta aad baahato u jawaab, ka dibna /broadcast qor.**")
        return

    status   = await message.reply("📢 **Fariinta la dirayo...**")
    ids      = await get_all_user_ids()
    success  = 0
    failed   = 0

    for uid in ids:
        try:
            await message.reply_to_message.copy(uid)
            success += 1
            await asyncio.sleep(0.05)  # avoid flood
        except Exception:
            failed += 1

    await status.edit(
        f"✅ **Broadcast dhammaaday!**\n\n"
        f"• La diray: `{success}`\n"
        f"• Ku fashilmay: `{failed}`"
    )


@Client.on_message(filters.command("warn") & admin_filter)
@admin_only
async def cmd_warn(client: Client, message: Message):
    parts = message.text.split(None, 2)
    if len(parts) < 3:
        await message.reply("**Isticmaal:** `/warn USER_ID fariiintaada`")
        return
    try:
        target_id = int(parts[1])
        text      = parts[2]
        await client.send_message(target_id, f"⚠️ **Digniin Admin:**\n\n{text}")
        await message.reply(f"✅ Digniin loo diray `{target_id}`.")
    except Exception as e:
        await message.reply(f"❌ Khalad: `{e}`")


@Client.on_message(filters.command("addpremium") & admin_filter)
@admin_only
async def cmd_add_premium(client: Client, message: Message):
    from datetime import datetime, timedelta
    parts = message.text.split()
    if len(parts) < 3:
        await message.reply("**Isticmaal:** `/addpremium USER_ID DAYS`")
        return
    try:
        uid     = int(parts[1])
        days    = int(parts[2])
        expires = datetime.utcnow() + timedelta(days=days)
        await add_premium(uid, "premium", expires)
        await message.reply(f"✅ Premium waa la daray `{uid}` ({days} maalmood).")
        await client.send_message(uid, f"🎉 **Premium-kaaga waa la kucdaray!**\n📅 Waxay dhacaysaa: {expires.strftime('%Y-%m-%d')}")
    except Exception as e:
        await message.reply(f"❌ Khalad: `{e}`")


@Client.on_message(filters.command("resetpower") & admin_filter)
@admin_only
async def cmd_reset_power(client: Client, message: Message):
    parts = message.text.split()
    if len(parts) < 2:
        await message.reply("**Isticmaal:** `/resetpower USER_ID`")
        return
    await remove_premium(int(parts[1]))
    await message.reply(f"♻️ Power dib loo celiyay `{parts[1]}`.")


@Client.on_message(filters.command("ban") & admin_filter)
@admin_only
async def cmd_ban(client: Client, message: Message):
    parts = message.text.split()
    if len(parts) < 2:
        await message.reply("**Isticmaal:** `/ban USER_ID`")
        return
    await ban_user(int(parts[1]))
    await message.reply(f"🚫 Isticmaalaha `{parts[1]}` waa la xidday.")


@Client.on_message(filters.command("unban") & admin_filter)
@admin_only
async def cmd_unban(client: Client, message: Message):
    parts = message.text.split()
    if len(parts) < 2:
        await message.reply("**Isticmaal:** `/unban USER_ID`")
        return
    await unban_user(int(parts[1]))
    await message.reply(f"✅ Isticmaalaha `{parts[1]}` waa la xoroobiyay.")


@Client.on_message(filters.command("restart") & admin_filter)
@admin_only
async def cmd_restart(client: Client, message: Message):
    await message.reply("♻️ **Bot-ka dib ayaa loo bilaabayaa...**")
    import os, sys
    os.execl(sys.executable, sys.executable, *sys.argv)


@Client.on_message(filters.command("maintenance") & admin_filter)
@admin_only
async def cmd_maintenance(client: Client, message: Message):
    import config
    config.MAINTENANCE_MODE = not config.MAINTENANCE_MODE
    state = "✅ FURAN" if config.MAINTENANCE_MODE else "❌ XIDHAN"
    await message.reply(f"🔧 **Nabad-sugidda:** {state}")