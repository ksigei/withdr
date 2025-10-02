import requests
from decimal import Decimal

def get_conversion_rate(crypto: str, fiat: str = "USD") -> Decimal:
    """
    Fetch crypto->fiat rate from CoinGecko API.
    """
    url = f"https://api.coingecko.com/api/v3/simple/price"
    params = {"ids": crypto.lower(), "vs_currencies": fiat.lower()}
    r = requests.get(url, params=params)
    data = r.json()
    return Decimal(str(data[crypto.lower()][fiat.lower()]))
