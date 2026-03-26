from flask import Blueprint, request, jsonify
from datetime import datetime
from db import alerts_collection
from utils.parser import parse_payload

webhook_bp = Blueprint("webhook", __name__)

@webhook_bp.route("", methods=["POST"])
def receive_webhook():
    data = parse_payload(request)

    document = {
        "received_at": datetime.utcnow(),
        "type": data.get("type"),
        "symbol": data.get("symbol"),
        "trade_id": data.get("trade_id"),   # ⭐ ADD THIS
        "timestamp": data.get("timestamp"), # ⭐ ADD THIS
        "raw": data
    }

    alerts_collection.insert_one(document)

    return jsonify({"status": "success"})