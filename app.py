from flask import Flask, request, jsonify
from datetime import datetime, timezone
from config import Config
from db import alerts_collection

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

    doc = {
        'received_at': datetime.now(timezone.utc),
        'content_type': content_type,
        'headers': dict(request.headers),
        'query_params': request.args.to_dict(),
        'parsed_payload': parsed,

        # ✅ FIX HERE (store as string instead of bytes)
        'raw_payload': request.get_data(as_text=True),

        'source_ip': request.remote_addr,
        'user_agent': request.user_agent.string
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

    cursor = alerts_collection.find().sort('received_at', -1).skip(skip).limit(limit)
    data = [serialize_mongo(d) for d in cursor]

    total = alerts_collection.count_documents({})

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