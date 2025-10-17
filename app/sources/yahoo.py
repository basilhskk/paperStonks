import yfinance as yf


def fetch(symbol: str):
    t = yf.Ticker(symbol)
    info = t.fast_info
    price = float(info['last_price'])
    prev = float(info['previous_close'])
    change_pct = (price - prev) / prev * 100 if prev else 0.0
    return {
    'symbol': symbol,
    'price': price,
    'change_pct': change_pct,
    }