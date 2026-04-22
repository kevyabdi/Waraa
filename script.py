from config import BOT_NAME

# ════════════════════════════════════════════
#       WARAA BOT — UI TEXT TEMPLATES
# ════════════════════════════════════════════


class Script:

    # ── Start / Welcome ──────────────────────
    START_TXT = """👋 <b>Salaam, {}!</b>

🤖 <b>Waraa Bot</b> waa bot aad ugu xawli badan oo loogu talagalay in aad ku magacaabto faylashaada Telegram.

📌 <b>Waxa aad samayn kartaa:</b>
• Faylasha magacood beddel
• Thumbnail custom ah ku kaydi
• Caption gaar ah ku dar
• Metadata ku qor faylashaada

⚡ Bilow adigoo i soo diraaya <b>fayl</b> kasta!"""

    # ── Help ─────────────────────────────────
    HELP_TXT = """📖 <b>CAAWIMO — Amarka dhan</b>

<b>👤 Isticmaalaha:</b>
/start — Bilow bot-ka
/viewthumb — Arag thumbnail-kaaga
/delthumb — Tirtir thumbnail-kaaga
/set_caption — Dejiso caption
/see_caption — Arag caption-kaaga
/del_caption — Tirtir caption
/ping — Xawliga bot-ka hubi
/myplan — Qorshahaga arag
/stats — Xogahaaga arki

<b>🆕 Cusub:</b>
/autodelete — Gali/dami tirtirka tooska ah
/setmetadata — Metadata u dejiso faylashaada
/language — Luuqadda dooro"""

    # ── Thumbnail ────────────────────────────
    THUMBNAIL_TXT = """🖼️ <b>SID LOOGU DARO THUMBNAIL</b>

<b>①</b> Sawir igu soo dir si toos ah.
<b>②</b> Bot-ku wuxuu ku kaydin doonaa.
<b>③</b> Faylka aad rename garayso wuxuu isticmaali doonaa thumbnail-kaaga.

/viewthumb — Arag thumbnail-kaaga hadda
/delthumb  — Tirtir thumbnail-kaaga"""

    # ── Caption ──────────────────────────────
    CAPTION_TXT = """📝 <b>SID LOOGU DARO CAPTION</b>

<b>Dooro:</b>
• <code>{filename}</code> — Magaca faylka
• <code>{filesize}</code> — Cabbirka faylka
• <code>{duration}</code> — Muddada (video/audio)

<b>Tusaale:</b>
<code>🎬 {filename} | 📦 {filesize}</code>

/set_caption — Dejiso caption-kaaga
/see_caption — Arag caption-kaaga
/del_caption — Tirtir"""

    # ── About ────────────────────────────────
    ABOUT_TXT = f"""ℹ️ <b>WARAA BOT — XOGTA</b>

🤖 <b>Magaca:</b> {BOT_NAME}
🐍 <b>Luuqadda:</b> <a href='https://python.org'>Python 3</a>
📚 <b>Maktabadda:</b> <a href='https://pyrogram.org'>Pyrogram 2.0</a>
💾 <b>DB:</b> MongoDB Atlas
🔧 <b>Loo sameeyay:</b> Waraa Project"""

    # ── Plan ─────────────────────────────────
    PLAN_TXT = """🎯 <b>QORSHAHAGA HADDA</b>

👤 <b>Isticmaale:</b> {}
📦 <b>Qorshaha:</b> {}
📊 <b>Xadka faylka:</b> {}
📅 <b>Xilliga dhacaya:</b> {}"""

    # ── Admin Commands ───────────────────────
    ADMIN_TXT = """🔐 <b>ADMIN AMARRADA</b>

/users        — Isticmaalayaasha oo dhan
/allids       — IDs-yada isticmaalayaasha
/broadcast    — Fariin u dir dadka oo dhan
/warn         — Isticmaale gaar ah u digso
/addpremium   — Premium ku dar isticmaale
/resetpower   — Power dib u celi (2GB)
/ceasepower   — Power hoos u dhig
/restart      — Bot-ka dib u bilow
/maintenance  — Nabad-sugidda gali/dami
/stats        — Xog guud oo bot-ka ah"""

    # ── Rename Prompts ───────────────────────
    RENAME_TXT     = "✏️ <b>Magaca cusub u qor faylka:</b>\n\n📄 <code>{}</code>"
    RENAME_WAIT    = "⏳ <b>Waxaa la shaqaynayaa...</b> Fadlan sug."
    RENAME_DONE    = "✅ <b>Magaca waa la beddelay!</b>\n\n📄 <code>{}</code>"
    RENAME_FAILED  = "❌ <b>Cilad ayaa dhacday.</b> Dib u isku day."

    # ── Errors ───────────────────────────────
    FLOOD_WAIT     = "⏱️ <b>Xawli badan!</b> {} ilbiriqsi ka dib isku day."
    FORCE_SUB_TXT  = "🔔 <b>Channel-ka nagu soo biir marka hore:</b>\n👉 {}"
    MAINTENANCE_TXT = "🔧 <b>Bot-ku wuxuu ku jiraa waqtiga dayactirka.</b>\nFadlan mar dambe isku day."
    NO_PLAN_TXT    = "🚫 <b>Premium ma lihid.</b> Isticmaal /upgrade si aad u hesho."

    # ── NEW: Auto-Delete ─────────────────────
    AUTO_DELETE_TXT = "🗑️ <b>Faylkani wuxuu is-tirtirayaa {} ilbiriqsi gudahood.</b>"

    # ── NEW: Stats ───────────────────────────
    STATS_TXT = """📊 <b>XOGAHAAGA</b>

👤 <b>ID:</b> <code>{user_id}</code>
📁 <b>Guud ahaan la rename gareeyay:</b> {total_renamed}
🗓️ <b>Maanta:</b> {today_renamed}
💾 <b>Faylasha ugu waaweyn:</b> {largest_file}
📅 <b>Xubin noqday:</b> {joined_date}"""

    # ── NEW: Language Menu ───────────────────
    LANG_TXT = """🌐 <b>LUUQADDA DOORO</b>

Luuqadda aad doonayso xulo:"""