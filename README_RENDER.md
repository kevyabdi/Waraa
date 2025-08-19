# Render Deploy (Web Service) – Telegram Rename Bot

This package is configured to run on Render as a **web service** exactly like your working Inline10 setup.

## Deploy Steps

1. Create a new **Web Service** on Render.
2. Connect this repo / upload the zip.
3. Render will use:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `bash -lc 'python3 bot.py & gunicorn app:app -b 0.0.0.0:$PORT'`
4. Set the Environment Variables (ENV): 
   - `API_ID`, `API_HASH`, `BOT_TOKEN`, `ADMIN`
   - `DATABASE_URL` (MongoDB connection) and `DATABASE_NAME` (e.g., `rename_bot`)
   - Optional: `LOG_CHANNEL`, `FORCE_SUBS`, `STRING_SESSION`, `START_PIC`, `SHORTNER_URL`, `SHORTNER_API`, `TOKEN_TIMEOUT`
5. Deploy. The web health check at `/` will return a simple message if the service is up.

> Notes
- You **do not** need a Background Worker on Render – the bot runs alongside the Flask keepalive inside one web service.
- `gunicorn` serves the Flask app and binds to the `$PORT` Render provides.
