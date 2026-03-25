from flask import Blueprint, request, jsonify
from services.normalizer import normalize_payload
from services.trade_manager import handle_trade
from services.metadata_builder import build_metadata
from db import alerts_collection

webhook_bp = Blueprint("webhook", __name__)

@webhook_bp.route("/", methods=["POST"])
def webhook():
    data = request.get_json()

    normalized = normalize_payload(data)
    meta = build_metadata(normalized)

    alerts_collection.insert_one({
        **normalized,
        "meta": meta
    })

    result = handle_trade(normalized, meta)

    return jsonify({"status": "ok", "result": str(result)})
