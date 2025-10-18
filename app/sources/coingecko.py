import requests


def fetch(symbol: str):
    # Expect symbols like BTC-USD, ETH-USD
    base = symbol.split('-')[0].lower()
    r = requests.get(
    'https://api.coingecko.com/api/v3/simple/price',
    params={'ids': base, 'vs_currencies': 'usd', 'include_24hr_change': 'true'}, timeout=8
    )
    j = r.json()
    print(j)
    price = float(j[base]['usd'])
    change_pct = float(j[base]['usd_24h_change'])
    return {
    'symbol': symbol,
    'price': price,
    'change_pct': change_pct,
    }