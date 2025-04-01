import requests
import json


class APIException(Exception):
    pass


class CurrencyConverter:
    @staticmethod
    def get_price(base, quote, amount):
        if base == quote:
            raise APIException(f'Невозможно перевести одинаковые валюты: {base}.')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Количество должно быть числом.')

        url = f'https://api.exchangerate-api.com/v4/latest/{base}'
        response = requests.get(url)

        if response.status_code != 200:
            raise APIException(f'Ошибка получения данных: {response.status_code}')

        data = response.json()

        if quote not in data['rates']:
            raise APIException(f'Валюта {quote} не найдена.')

        rate = data['rates'][quote]
        total_amount = rate * amount
        return total_amount