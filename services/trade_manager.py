from db import trades_collection
from datetime import datetime

def handle_trade(data, meta):
    if data["type"] == "BUY":
        return create_trade(data, meta)
    elif data["type"] == "SELL":
        return close_trade(data)

def create_trade(data, meta):
    trade = {
        "symbol": data["symbol"],
        "status": "OPEN",
        "buy": {
            "price": data["price"],
            "time": data["datetime"],
            "timestamp": data["timestamp"],
            "volume": data["volume"]
        },
        "meta": meta,
        "history": data["history"],
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    return trades_collection.insert_one(trade)

def close_trade(data):
    trade = trades_collection.find_one(
        {"symbol": data["symbol"], "status": "OPEN"},
        sort=[("created_at", -1)]
    )

    if not trade:
        return {"msg": "No open trade found"}

    pnl = data["price"] - trade["buy"]["price"]
    pnl_percent = (pnl / trade["buy"]["price"]) * 100

    trades_collection.update_one(
        {"_id": trade["_id"]},
        {
            "$set": {
                "status": "CLOSED",
                "sell": {
                    "price": data["price"],
                    "time": data["datetime"],
                    "timestamp": data["timestamp"]
                },
                "pnl": pnl,
                "pnl_percent": pnl_percent,
                "updated_at": datetime.utcnow()
            }
        }
    )

    return {"msg": "Trade closed"}
