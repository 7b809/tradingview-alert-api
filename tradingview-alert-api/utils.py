from db import signals_collection


def find_open_buy(symbol, interval):
    return signals_collection.find_one(
        {
            'symbol': symbol,
            'interval': interval,
            'type': 'BUY',
            'status': 'OPEN'
        },
        sort=[('timestamp', -1)]
    )


def close_trade(buy_id, sell_doc):
    signals_collection.update_one(
        {'_id': buy_id},
        {
            '$set': {
                'status': 'MATCHED',
                'sell': sell_doc
            }
        }
    )
