import logging
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient

from config import DATABASE_URL, DATABASE_NAME

# ════════════════════════════════════════════
#       WARAA BOT — DATABASE HELPER
# ════════════════════════════════════════════

logger = logging.getLogger("waraa.db")

_client = AsyncIOMotorClient(DATABASE_URL)
db      = _client[DATABASE_NAME]

users_col    = db["users"]
premium_col  = db["premium"]
settings_col = db["settings"]
stats_col    = db["stats"]        # NEW: rename stats per user


# ── User Management ──────────────────────────

async def add_user(user_id: int) -> None:
    """Add a new user if they don't exist yet."""
    if not await users_col.find_one({"id": user_id}):
        await users_col.insert_one({
            "id":           user_id,
            "joined":       datetime.utcnow(),
            "total_renamed": 0,
            "banned":       False,
        })
        logger.info("New user added: %d", user_id)


async def get_all_users():
    return users_col.find({})


async def get_user_count() -> int:
    return await users_col.count_documents({})


async def get_all_user_ids() -> list[int]:
    cursor = users_col.find({}, {"id": 1})
    return [doc["id"] async for doc in cursor]


async def ban_user(user_id: int) -> None:
    await users_col.update_one({"id": user_id}, {"$set": {"banned": True}}, upsert=True)


async def unban_user(user_id: int) -> None:
    await users_col.update_one({"id": user_id}, {"$set": {"banned": False}})


async def is_banned(user_id: int) -> bool:
    doc = await users_col.find_one({"id": user_id})
    return bool(doc and doc.get("banned"))


# ── Thumbnail ────────────────────────────────

async def set_thumbnail(user_id: int, file_id: str) -> None:
    await settings_col.update_one(
        {"id": user_id},
        {"$set": {"thumbnail": file_id}},
        upsert=True
    )


async def get_thumbnail(user_id: int) -> str | None:
    doc = await settings_col.find_one({"id": user_id})
    return doc.get("thumbnail") if doc else None


async def del_thumbnail(user_id: int) -> None:
    await settings_col.update_one({"id": user_id}, {"$unset": {"thumbnail": ""}})


# ── Caption ──────────────────────────────────

async def set_caption(user_id: int, caption: str) -> None:
    await settings_col.update_one(
        {"id": user_id},
        {"$set": {"caption": caption}},
        upsert=True
    )


async def get_caption(user_id: int) -> str | None:
    doc = await settings_col.find_one({"id": user_id})
    return doc.get("caption") if doc else None


async def del_caption(user_id: int) -> None:
    await settings_col.update_one({"id": user_id}, {"$unset": {"caption": ""}})


# ── Premium ──────────────────────────────────

async def add_premium(user_id: int, plan: str, expires: datetime) -> None:
    await premium_col.update_one(
        {"id": user_id},
        {"$set": {"plan": plan, "expires": expires, "active": True}},
        upsert=True
    )


async def get_premium(user_id: int) -> dict | None:
    return await premium_col.find_one({"id": user_id})


async def remove_premium(user_id: int) -> None:
    await premium_col.update_one({"id": user_id}, {"$set": {"active": False}})


async def is_premium(user_id: int) -> bool:
    doc = await premium_col.find_one({"id": user_id, "active": True})
    if not doc:
        return False
    if doc.get("expires") and doc["expires"] < datetime.utcnow():
        await remove_premium(user_id)
        return False
    return True


# ── NEW: Rename Stats ────────────────────────

async def increment_rename(user_id: int, file_size: int = 0) -> None:
    today = datetime.utcnow().strftime("%Y-%m-%d")
    await stats_col.update_one(
        {"id": user_id},
        {
            "$inc": {
                "total_renamed": 1,
                f"daily.{today}": 1,
                "total_bytes": file_size,
            },
            "$max": {"largest_file": file_size},
        },
        upsert=True
    )
    await users_col.update_one(
        {"id": user_id},
        {"$inc": {"total_renamed": 1}}
    )


async def get_user_stats(user_id: int) -> dict:
    doc = await stats_col.find_one({"id": user_id}) or {}
    today = datetime.utcnow().strftime("%Y-%m-%d")
    user  = await users_col.find_one({"id": user_id}) or {}
    return {
        "user_id":       user_id,
        "total_renamed": doc.get("total_renamed", 0),
        "today_renamed": doc.get("daily", {}).get(today, 0),
        "largest_file":  _fmt_size(doc.get("largest_file", 0)),
        "joined_date":   user.get("joined", "—"),
    }


# ── NEW: Metadata ────────────────────────────

async def set_metadata(user_id: int, metadata: str) -> None:
    await settings_col.update_one(
        {"id": user_id},
        {"$set": {"metadata": metadata}},
        upsert=True
    )


async def get_metadata(user_id: int) -> str | None:
    doc = await settings_col.find_one({"id": user_id})
    return doc.get("metadata") if doc else None


# ── NEW: Auto-Delete ─────────────────────────

async def set_auto_delete(user_id: int, seconds: int) -> None:
    await settings_col.update_one(
        {"id": user_id},
        {"$set": {"auto_delete": seconds}},
        upsert=True
    )


async def get_auto_delete(user_id: int) -> int:
    doc = await settings_col.find_one({"id": user_id})
    return doc.get("auto_delete", 0) if doc else 0


# ── Helpers ──────────────────────────────────

def _fmt_size(size: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} TB"