import time
import math
import logging
import asyncio
from functools import wraps
from collections import defaultdict

from pyrogram.types import Message
from config import ADMIN, MAX_RENAME_PER_MINUTE, MAINTENANCE_MODE

logger = logging.getLogger("waraa.utils")

# ════════════════════════════════════════════
#       WARAA BOT — UTILITY HELPERS
# ════════════════════════════════════════════


# ── File Size Formatter ──────────────────────

def humanbytes(size: int) -> str:
    if size == 0:
        return "0 B"
    units = ("B", "KB", "MB", "GB", "TB")
    i = int(math.floor(math.log(size, 1024)))
    p = math.pow(1024, i)
    return f"{size / p:.2f} {units[min(i, len(units)-1)]}"


# ── Time Formatter ───────────────────────────

def time_formatter(seconds: int) -> str:
    minutes, secs = divmod(int(seconds), 60)
    hours, mins   = divmod(minutes, 60)
    if hours:
        return f"{hours}s {mins}d {secs}s"
    if mins:
        return f"{mins}d {secs}s"
    return f"{secs}s"


# ── Progress Bar ─────────────────────────────

async def progress_bar(current: int, total: int, message: Message,
                       text: str, start_time: float) -> None:
    if total == 0:
        return
    pct      = current * 100 / total
    filled   = int(pct / 5)
    bar      = "█" * filled + "░" * (20 - filled)
    elapsed  = time.time() - start_time
    speed    = current / elapsed if elapsed > 0 else 0
    eta      = (total - current) / speed if speed > 0 else 0

    try:
        await message.edit(
            f"{text}\n\n"
            f"[{bar}] {pct:.1f}%\n\n"
            f"📦 **{humanbytes(current)}** / **{humanbytes(total)}**\n"
            f"⚡ **{humanbytes(speed)}/s**\n"
            f"⏱️ ETA: **{time_formatter(eta)}**"
        )
    except Exception:
        pass


# ── Rate Limiter ─────────────────────────────

_user_requests: dict[int, list[float]] = defaultdict(list)


def is_rate_limited(user_id: int) -> bool:
    """Return True if this user has exceeded MAX_RENAME_PER_MINUTE."""
    if user_id in ADMIN:
        return False
    now    = time.time()
    window = 60.0
    reqs   = [t for t in _user_requests[user_id] if now - t < window]
    _user_requests[user_id] = reqs
    if len(reqs) >= MAX_RENAME_PER_MINUTE:
        return True
    _user_requests[user_id].append(now)
    return False


# ── Decorators ───────────────────────────────

def admin_only(func):
    """Restrict a handler to admins only."""
    @wraps(func)
    async def wrapper(client, message: Message, *args, **kwargs):
        if message.from_user.id not in ADMIN:
            await message.reply("🚫 Bu amarka adminku keliya isticmaali karaa.")
            return
        return await func(client, message, *args, **kwargs)
    return wrapper


def maintenance_check(func):
    """Block non-admins during maintenance mode."""
    @wraps(func)
    async def wrapper(client, message: Message, *args, **kwargs):
        if MAINTENANCE_MODE and message.from_user.id not in ADMIN:
            await message.reply(
                "🔧 **Bot-ku wuxuu ku jiraa waqtiga dayactirka.**\n"
                "Fadlan mar dambe isku day."
            )
            return
        return await func(client, message, *args, **kwargs)
    return wrapper


def rate_limit(func):
    """Apply per-user rate limiting."""
    @wraps(func)
    async def wrapper(client, message: Message, *args, **kwargs):
        if is_rate_limited(message.from_user.id):
            await message.reply(
                f"⏱️ **Xawli badan!** Daqiiqad gudahood {MAX_RENAME_PER_MINUTE} "
                "faylka kaliya rename garayn kartaa. Wax yar sug."
            )
            return
        return await func(client, message, *args, **kwargs)
    return wrapper


# ── Auto-Delete Helper ───────────────────────

async def auto_delete_message(message: Message, delay: int) -> None:
    """Delete a message after `delay` seconds."""
    if delay <= 0:
        return
    await asyncio.sleep(delay)
    try:
        await message.delete()
    except Exception:
        pass