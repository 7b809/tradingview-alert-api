def build_signal(doc):
    return {
        'webhook_id': doc.get('webhook_id'),
        'type': doc.get('type'),
        'symbol': doc.get('symbol'),
        'exchange': doc.get('exchange'),
        'interval': doc.get('interval'),
        'price': float(doc.get('price')),
        'volume_current': int(doc.get('volume_current')),
        'volume_previous': int(doc.get('volume_previous')),
        'ohlc': {
            'open': float(doc.get('open')),
            'high': float(doc.get('high')),
            'low': float(doc.get('low')),
            'close': float(doc.get('close')),
        },
        'candle_type': doc.get('candle_type'),
        'body_size': float(doc.get('body_size')),
        'range': float(doc.get('range')),
        'datetime': doc.get('datetime'),
        'timestamp': int(doc.get('timestamp')),
        'trigger_timestamp': int(doc.get('trigger_timestamp')),
        'history': doc.get('history', []),
        'status': 'OPEN'
    }
