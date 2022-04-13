import json
import requests
from Config import exchanger
class APIException(Exception):
    pass
class Convertor:
    @staticmethod
    def get_price(values):
        if len(values) != 3:
            raise APIException("Неверное количество параметров")
        quote, base, amount = values

        if quote == base:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}')

        try:
            quote_formatted = exchanger[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote}')

        try:
            base_formatted = exchanger[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}')


        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_formatted}&tsyms={base_formatted}')
        print(r)

        result = float(json.loads(r.content)[base_formatted]) * amount
        return round(result, 3)
