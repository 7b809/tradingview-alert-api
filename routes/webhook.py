from flask import Blueprint, request, jsonify
from datetime import datetime
from db import alerts_collection
from utils.parser import parse_payload

webhook_bp = Blueprint("webhook", __name__)

@webhook_bp.route("", methods=["POST"])
def receive_webhook():
    data = parse_payload(request)

    # document = {
    #     "received_at": datetime.utcnow(),
    #     "webhook_id": data.get("webhook_id"),
    #     "type": data.get("type"),
    #     "symbol": data.get("symbol"),
    #     "exchange": data.get("exchange"),
    #     "interval": data.get("interval"),
    #     "price": data.get("price"),
    #     "signal": data.get("signal"),
    #     "volume_current": data.get("volume_current"),
    #     "volume_previous": data.get("volume_previous"),
    #     "open": data.get("open"),
    #     "high": data.get("high"),
    #     "low": data.get("low"),
    #     "close": data.get("close"),
    #     "candle_type": data.get("candle_type"),
    #     "datetime": data.get("datetime"),
    #     "timestamp": data.get("timestamp"),
    #     "raw": data
    # }
    document = {
        "received_at": datetime.utcnow(),       
        "raw": data
    }

    alerts_collection.insert_one(document)

    return jsonify({"status": "success"})