import pybit
from pybit import usdt_perpetual

session = usdt_perpetual.HTTP(
    endpoint='https://api-testnet.bybit.com',
    api_key='ePZaJUACu5suh6pf1t',
    api_secret='hOjlvuGTtqyXtd9odO9Mt3j3ZiDVtc30vtwd'
)

# print(session.get_wallet_balance(coin='USDT'))


def place_order(symbol, side, qty):
    return session.place_active_order(
        symbol=symbol,
        side=side,
        order_type="Market",
        qty=qty,
        time_in_force="GoodTillCancel",
        reduce_only=False,
        close_on_trigger=False
    )


def close_order(symbol, side, qty):
    return session.place_active_order(
        symbol=symbol,
        side=side,
        order_type="Market",
        qty=qty,
        time_in_force="GoodTillCancel",
        reduce_only=True,
        close_on_trigger=False
    )
