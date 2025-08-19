import os

# Required Variables Config
API_ID = int(os.environ.get("API_ID", "0"))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
ADMIN = int(os.environ.get("ADMIN", "0"))

# Premium 4GB Renaming Client Config (optional)
STRING_SESSION = os.environ.get("STRING_SESSION", "")

# Log & Force Channel Config (optional)
LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "0")) if os.environ.get("LOG_CHANNEL") else None
FORCE_SUBS = os.environ.get("FORCE_SUBS", "") or None

# Database (MongoDB Atlas) Config
DATABASE_URL = os.environ.get("DATABASE_URL", "")
DATABASE_NAME = os.environ.get("DATABASE_NAME", "rename_bot")

# Assets / UI (optional)
START_PIC = os.environ.get("START_PIC", "") or None

# Optional shortener settings
SHORTNER_URL = os.environ.get("SHORTNER_URL", "") or None
SHORTNER_API = os.environ.get("SHORTNER_API", "") or None
TOKEN_TIMEOUT = os.environ.get("TOKEN_TIMEOUT", "") or None
