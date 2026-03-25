def normalize_payload(data):
    return {
        "type": data.get("type"),
        "symbol": data.get("symbol"),
        "price": float(data.get("price", 0)),
        "timestamp": int(data.get("timestamp", 0)),
        "datetime": data.get("datetime"),
        "volume": data.get("volume_current"),
        "interval": data.get("interval"),
        "candle_type": data.get("candle_type"),
        "body_size": float(data.get("body_size", 0)),
        "range": float(data.get("range", 0)),
        "history": data.get("history", [])
    }
