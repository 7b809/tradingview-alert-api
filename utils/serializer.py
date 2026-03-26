def serialize(doc):
    raw = doc.get("raw", {})

    return {
        "id": str(doc["_id"]),
        "type": raw.get("type"),
        "symbol": raw.get("symbol"),
        "trade_id": raw.get("trade_id"),   # ⭐ IMPORTANT
        "price": raw.get("price"),
        "timestamp": raw.get("timestamp"),
        "datetime": raw.get("datetime"),
        "count": raw.get("count"),
        "signal": raw.get("signal"),

        # optional (keep raw if needed)
        "raw": raw
    }