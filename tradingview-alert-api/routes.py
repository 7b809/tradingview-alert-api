from flask import Blueprint, request, jsonify
from db import signals_collection
from models import build_signal
from utils import find_open_buy, close_trade

webhook = Blueprint('webhook', __name__)

@webhook.route('/webhook', methods=['POST'])
def tradingview_webhook():
    try:
        data = request.get_json(force=True)
        signal_type = data.get('type')
        symbol = data.get('symbol')
        interval = data.get('interval')

        if not signal_type or not symbol:
            return jsonify({'error': 'Invalid payload'}), 400

        signal_doc = build_signal(data)

        if signal_type == 'BUY':
            signals_collection.insert_one(signal_doc)
            return jsonify({'status': 'BUY stored'}), 200

        if signal_type == 'SELL':
            open_buy = find_open_buy(symbol, interval)
            if open_buy:
                close_trade(open_buy['_id'], signal_doc)
                return jsonify({'status': 'SELL matched'}), 200
            else:
                signal_doc['status'] = 'UNMATCHED'
                signals_collection.insert_one(signal_doc)
                return jsonify({'status': 'SELL stored without BUY'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500



@webhook.route('/alerts', methods=['GET'])
@webhook.route('/alerts/<int:page>', methods=['GET'])
def get_alerts(page=1):
    try:
        PER_PAGE = 25

        skip = (page - 1) * PER_PAGE

        # Fetch alerts (latest first)
        cursor = signals_collection.find().sort('_id', -1).skip(skip).limit(PER_PAGE)

        alerts = []
        for doc in cursor:
            doc['_id'] = str(doc['_id'])
            alerts.append(doc)

        total_count = signals_collection.count_documents({})
        total_pages = (total_count + PER_PAGE - 1) // PER_PAGE

        return jsonify({
            'page': page,
            'per_page': PER_PAGE,
            'total': total_count,
            'total_pages': total_pages,
            'data': alerts
        }), 200

    except Exception as e:

        return jsonify({'error': str(e)}), 500
    
    
@webhook.route('/', methods=['GET'])
def home():
    return jsonify({
        "message": "TradingView Webhook API is running 🚀",
        "routes": {
            "POST /webhook": "Receive TradingView alerts",
            "GET /alerts": "Get alerts (page 1)",
            "GET /alerts/<page>": "Paginated alerts"
        }
    }), 200    