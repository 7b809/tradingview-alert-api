from flask import Flask, request, jsonify
from datetime import datetime, timezone
from config import Config
from db import alerts_collection

# ✅ NEW IMPORTS (added only)
import json
import re

app = Flask(__name__)


def serialize_mongo(doc):
    doc['_id'] = str(doc['_id'])

    # ✅ FIX: convert bytes → string (prevents JSON error)
    if isinstance(doc.get('raw_payload'), bytes):
        doc['raw_payload'] = doc['raw_payload'].decode('utf-8', errors='replace')

    return doc


def parse_request_payload(req):
    content_type = req.content_type or 'unknown'

    if req.is_json:
        payload = req.get_json(silent=True)

    elif content_type.startswith('application/x-www-form-urlencoded') or content_type.startswith('multipart/form-data'):
        payload = req.form.to_dict()

    else:
        payload = req.get_data(as_text=True)

    return content_type, payload


# ==============================
# ✅ NEW FUNCTION (NO CHANGE TO EXISTING)
# ==============================
def extract_fields(parsed_payload, raw_payload):
    symbol = None
    signal = None

    try:
        # Case 1: dict
        if isinstance(parsed_payload, dict):
            symbol = parsed_payload.get("symbol")
            signal = parsed_payload.get("type") or parsed_payload.get("signal")

        # Case 2: string JSON
        elif isinstance(parsed_payload, str):
            try:
                data = json.loads(parsed_payload)
                symbol = data.get("symbol")
                signal = data.get("type") or data.get("signal")
            except:
                pass

        # Case 3: fallback from raw text
        if not symbol and raw_payload:
            match = re.search(r'(BTCUSD|NIFTY|BANKNIFTY)', raw_payload)
            if match:
                symbol = match.group(1)

        if not signal and raw_payload:
            raw_upper = raw_payload.upper()
            if "BUY" in raw_upper:
                signal = "BUY"
            elif "SELL" in raw_upper:
                signal = "SELL"

    except Exception as e:
        print("Extraction error:", e)

    return symbol, signal


# ==============================
# HOME ROUTE
# ==============================
@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "status": "success",
        "message": "TradingView Alert API is running 🚀",
        "routes": {
            "POST /webhook": "Receive webhook alerts",
            "GET /alerts": "Fetch stored alerts (paginated)"
        }
    })


# ==============================
# WEBHOOK
# ==============================
@app.route('/webhook', methods=['POST'])
def webhook():
    content_type, parsed = parse_request_payload(request)

    # ✅ NEW: extract symbol & signal
    raw_data = request.get_data(as_text=True)
    symbol, signal = extract_fields(parsed, raw_data)

    doc = {
        'received_at': datetime.now(timezone.utc),
        'content_type': content_type,
        'headers': dict(request.headers),
        'query_params': request.args.to_dict(),
        'parsed_payload': parsed,

        # ✅ existing logic unchanged
        'raw_payload': raw_data,

        'source_ip': request.remote_addr,
        'user_agent': request.user_agent.string,

        # ✅ NEW FIELDS (added only)
        'symbol': symbol,
        'signal': signal
    }

    result = alerts_collection.insert_one(doc)

    return jsonify({
        'status': 'success',
        'alert_id': str(result.inserted_id)
    }), 201


# ==============================
# GET ALERTS
# ==============================
@app.route('/alerts', methods=['GET'])
def alerts():
    page = int(request.args.get('page', 1))
    limit = min(int(request.args.get('limit', 25)), 25)
    skip = (page - 1) * limit

    # ✅ NEW FILTERS (optional, does not break old logic)
    symbol = request.args.get('symbol')
    signal = request.args.get('signal')

    query = {}
    if symbol:
        query['symbol'] = symbol
    if signal:
        query['signal'] = signal

    cursor = alerts_collection.find(query).sort('received_at', -1).skip(skip).limit(limit)
    data = [serialize_mongo(d) for d in cursor]

    total = alerts_collection.count_documents(query)

    return jsonify({
        'page': page,
        'limit': limit,
        'total_records': total,
        'alerts': data
    })


# ==============================
# RUN
# ==============================
if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=Config.FLASK_PORT,
        debug=(Config.FLASK_ENV == 'development')
    )