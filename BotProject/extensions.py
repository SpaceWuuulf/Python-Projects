import requests
import json
from config import keys

class ConvertionException(Exception):
    pass

class CryptoConverter:
    @staticmethod
    def convert(quote: str, base: str, amount: str):
        if quote == base:
            raise ConvertionException(f'Невозможно перевести одинаковые валюты {base}')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Не удалось обработать количесвто {amount}')

        r = requests.get(
            f'https://min-api.cryptocompare.com/data/pricemulti?fsyms=BTC&tsyms={quote_ticker},{base_ticker}')
        first = json.loads(r.content)["BTC"][keys[base]]
        second = json.loads(r.content)["BTC"][keys[quote]]
        total_base = first / second * int(amount)

        return total_base