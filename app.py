import os
from flask import Flask, jsonify
from datetime import datetime

# ════════════════════════════════════════════
#       WARAA BOT — WEB HEALTH SERVER
# ════════════════════════════════════════════

app = Flask(__name__)
START_TIME = datetime.utcnow()


@app.route("/")
def index():
    uptime = str(datetime.utcnow() - START_TIME).split(".")[0]
    return jsonify({
        "bot":    "Waraa Bot",
        "status": "running",
        "uptime": uptime,
    })


@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)