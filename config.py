import os
import sys

# ════════════════════════════════════════════
#           WARAA BOT — CONFIGURATION
# ════════════════════════════════════════════

# ── Required Variables ──────────────────────
API_ID      = int(os.environ.get("API_ID", "0"))
API_HASH    = os.environ.get("API_HASH", "")
BOT_TOKEN   = os.environ.get("BOT_TOKEN", "")

# ADMIN can be a single ID or space-separated list
_admin_raw  = os.environ.get("ADMIN", "0")
ADMIN       = [int(x) for x in _admin_raw.split() if x.isdigit()]

# ── Database ────────────────────────────────
DATABASE_URL  = os.environ.get("DATABASE_URL", "")
DATABASE_NAME = os.environ.get("DATABASE_NAME", "waraa_bot")

# ── Premium / 4GB Client ────────────────────
STRING_SESSION = os.environ.get("STRING_SESSION", "") or None

# ── Channels ────────────────────────────────
LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "0")) if os.environ.get("LOG_CHANNEL") else None
FORCE_SUBS  = os.environ.get("FORCE_SUBS", "") or None

# ── UI / Assets ─────────────────────────────
START_PIC   = os.environ.get("START_PIC", "") or None
BOT_NAME    = os.environ.get("BOT_NAME", "Waraa Bot")

# ── Link Shortener (optional) ───────────────
SHORTNER_URL = os.environ.get("SHORTNER_URL", "") or None
SHORTNER_API = os.environ.get("SHORTNER_API", "") or None
TOKEN_TIMEOUT = int(os.environ.get("TOKEN_TIMEOUT", "0")) or None

# ── NEW: Auto-Delete Settings ───────────────
# Automatically delete renamed files after X seconds (0 = disabled)
AUTO_DELETE_TIME = int(os.environ.get("AUTO_DELETE_TIME", "0"))

# ── NEW: Rate Limiting ──────────────────────
# Max rename requests per user per minute
MAX_RENAME_PER_MINUTE = int(os.environ.get("MAX_RENAME_PER_MINUTE", "5"))

# ── NEW: Watermark / Metadata Branding ──────
DEFAULT_METADATA = os.environ.get("DEFAULT_METADATA", "") or None

# ── NEW: Maintenance Mode ───────────────────
MAINTENANCE_MODE = os.environ.get("MAINTENANCE_MODE", "false").lower() == "true"

# ════════════════════════════════════════════
#         STARTUP VALIDATION
# ════════════════════════════════════════════
_errors = []
if API_ID == 0:
    _errors.append("❌ API_ID is missing or invalid.")
if not API_HASH:
    _errors.append("❌ API_HASH is missing.")
if not BOT_TOKEN:
    _errors.append("❌ BOT_TOKEN is missing.")
if not DATABASE_URL:
    _errors.append("❌ DATABASE_URL is missing.")

if _errors:
    print("\n".join(_errors))
    print("\n⚠️  Please set all required environment variables before starting Waraa Bot.")
    sys.exit(1)