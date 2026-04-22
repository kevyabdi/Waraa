import asyncio
import logging
import pyrogram.utils
from pyrogram import Client, idle

from plugins.cb_data import app as premium_client
from config import (
    API_ID, API_HASH, BOT_TOKEN, STRING_SESSION, MAINTENANCE_MODE
)

# ════════════════════════════════════════════
#           WARAA BOT — ENTRY POINT
# ════════════════════════════════════════════

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("waraa")

# Allow large channel / group IDs
pyrogram.utils.MIN_CHAT_ID      = -999999999999
pyrogram.utils.MIN_CHANNEL_ID   = -100999999999999

# ── Main Bot Client ──────────────────────────
bot = Client(
    "Waraa",
    bot_token=BOT_TOKEN,
    api_id=API_ID,
    api_hash=API_HASH,
    plugins=dict(root="plugins"),
    sleep_threshold=60,        # retry flood-wait up to 60 s automatically
    max_concurrent_transmissions=5,
)


async def main() -> None:
    if MAINTENANCE_MODE:
        logger.warning("🔧 Bot is in MAINTENANCE MODE. Only admins can use it.")

    apps_to_run = [bot]

    if STRING_SESSION:
        logger.info("🚀 Starting with Premium 4GB client...")
        apps_to_run.insert(0, premium_client)

    try:
        for app in apps_to_run:
            await app.start()
            me = await app.get_me()
            logger.info("✅ Started: @%s (id=%d)", me.username, me.id)

        logger.info("🤖 Waraa Bot is now running. Press Ctrl+C to stop.")
        await idle()

    except Exception as exc:
        logger.exception("💥 Fatal error during startup: %s", exc)

    finally:
        logger.info("🛑 Shutting down gracefully...")
        for app in reversed(apps_to_run):
            try:
                await app.stop()
            except Exception:
                pass
        logger.info("👋 Waraa Bot stopped.")


if __name__ == "__main__":
    asyncio.run(main())