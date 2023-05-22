import logging
import os

import requests
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

URL = os.getenv('URL_EXCHANGE')


def get_currency_rates(url: str,
                       base: str = 'RUB',
                       symbols: str = 'USD,EUR,BGN',
                       amount: int = None) -> str:
    """Парсит курсы валют по заданному url."""
    try:
        response = requests.get(
            url,
            params={
                'base': base,
                'symbols': symbols,
            },
            allow_redirects=True
        )

        if response.status_code == 200:
            logger.info(f'Статус код от ресурса: {response.status_code}')
            data = response.json()
            if amount:
                logger.info(f'Запрос курсов с количеством валюты {amount}.')
                return '\n'.join(
                    [
                        f'{amount} {currency} = '
                        f'{(float(amount)/float(data["rates"].get(currency))):.2f} {base}'
                        for currency in data['rates'].keys()
                    ]
                )
            logger.info('Запрос конвертации без указания количества валюты.')
            return '\n'.join(
                [
                    f"{currency}/{base} - {(1/float(data['rates'].get(currency))):.2f}"
                    for currency in data['rates'].keys()
                ]
            )

    except Exception as e:
        logger.error(
            f'Ошибка подключения к ресурсу "{url}". Текст ошибки: {e}'
        )
        return (
            f'При попытке подключиться к ресурсу "{url}" '
            'возникла следующая ошибка - {e}'
        )
