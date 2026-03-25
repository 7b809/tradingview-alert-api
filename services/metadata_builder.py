def build_metadata(data):
    vol = data["volume"]
    body = data["body_size"]

    return {
        "trend": data["candle_type"],
        "vol_strength": "HIGH" if vol and vol > 100000 else "LOW",
        "body_strength": "STRONG" if body > 50 else "WEAK",
        "interval": data["interval"],
        "signal_source": "WaveTrend"
    }
