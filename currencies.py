import logging
import re
from typing import Union

from exceptions import UndefinedCurrency
from parsing_rates import URL, get_currency_rates

logger = logging.getLogger(__name__)


# top 25 the most traded currencies from website
# https://www.countries-ofthe-world.com/most-traded-currencies.html
COMMON_CURRENCIES = {'USD': 'US dollar',
                     'EUR': 'European Euro',
                     'JPY': 'Japanese yen',
                     'GBP': 'Pound sterling',
                     'AUD': 'Australian dollar',
                     'CAD': 'Canadian dollar',
                     'CHF': 'Swiss franc',
                     'CNY': 'Chinese Yuan Renminbi',
                     'SEK': 'Swedish krona',
                     'MXN': 'Mexican peso',
                     'NZD': 'New Zealand dollar',
                     'SGD': 'Singapore dollar',
                     'HKD': 'Hong Kong dollar',
                     'NOK': 'Norwegian krone',
                     'KRW': 'South Korean won',
                     'TRY': 'Turkish lira',
                     'INR': 'Indian rupee',
                     'RUB': 'Russian ruble',
                     'BRL': 'Brazilian real',
                     'ZAR': 'South African rand',
                     'DKK': 'Danish krone',
                     'PLN': 'Polish zloty',
                     'TWD': 'New Taiwan dollar',
                     'THB': 'Thai baht',
                     'MYR': 'Malaysian ringgit',
                     'BGN': 'Bulgarian leva',
                     'UAH': 'Ukrainian hryvnia'}


class Currencies:
    """Создает и хранит базовую валюту и другие."""

    def __init__(self) -> None:
        self._base_currency: str = ''
        self._other_currencies: set = set()

    def add_base(self, base: str) -> None:
        if base not in COMMON_CURRENCIES.keys():
            raise UndefinedCurrency(
                'Некорректно введен код валюты.'
            )
        self._base_currency = base.upper()

    def add_other_currency(self, other_currency: str) -> None:
        if other_currency not in COMMON_CURRENCIES.keys():
            logger.warning(
                f'Попытка ввода валюты {other_currency}, которой нет в списке'
            )
            raise UndefinedCurrency(
                'Некорректно введен код валюты.'
            )
        self._other_currencies.add(other_currency.upper())

    def return_base(self):
        return self._base_currency

    def return_other_currencies(self):
        return ','.join(self._other_currencies)

    def ready_for_repr(self):
        if self._base_currency and self._other_currencies:
            return True
        return False

    def clear(self):
        self._base_currency = ''
        self._other_currencies.clear()
        logger.info('Очистка прошлых значений атрибутов класса выполнена.')

    def __str__(self) -> str:
        return (
            f'base_currency: {self._base_currency}, '
            f'other_currencies: {self._other_currencies}'
        )


def write_currency(currency: Union[str, list], currencies: Currencies) -> None:
    """Делает запись в атрибуты экземпляра класса Currencies."""
    if isinstance(currency, list):
        logger.info('запись валюты в формате List.')
        currency = currency[0]
    if not currencies.return_base():
        currencies.add_base(currency)
        logger.info(f'Добавлена базовая валюта - {currency}')

    else:
        currencies.add_other_currency(currency)
        logger.info(f'Добавлена валюта для сравнения курса - {currency}')


def show_rates(currencies: Currencies, amount: str = None) -> str:
    """Показывает курсы валют для выбранных валютных пар."""
    logger.info(f'Выполнение с amount: {amount}')
    r = re.compile('^[0-9]+$')
    if amount is not None and not r.match(amount):
        logger.warning(f'Ошибка формата ввода валюты - {amount}.')
        return 'Была допущена ошибка ввода. Введите число'

    text = get_currency_rates(url=URL,
                              base=currencies.return_base(),
                              symbols=currencies.return_other_currencies(),
                              amount=amount)
    currencies.clear()
    return text


def no_currencies_chosen(url):
    """Показывает курсы валют дефолтных пар."""

    text = (
        'Ниже представлены актуальные курсы Евро, Доллара США и '
        'Болгарского Лева к рублю.'
    )
    return (f'{text}\n\n{get_currency_rates(url=url)}')


class UsersIdCurrencies:
    """
    Сохраняет список словарей с ключами user_id и currencies:
    user_id: int - id чата пользователя, который взаимодействует с ботом;
    currencies: Currencies - экземпляр класса Currencies.
    """

    def __init__(self) -> None:
        self._users_currencies: list[dict] = []

    def add_user_id(self, user_chat_id: int) -> None:
        logger.info(f'Добавлен новый id - пользователя: {user_chat_id}')
        if self.check_for_replica(user_chat_id):
            self._users_currencies.append(
                {
                    'user_id': user_chat_id,
                    'currencies': Currencies()
                }
            )

    def check_for_replica(self, user_chat_id: int):
        if not self._users_currencies:
            return True
        replica = [
            item for item in self._users_currencies
            if user_chat_id in item.values()
        ]

        if not replica:
            return True
        return False

    def add_currensies_to_user(self, user_chat_id: int, currency: str) -> None:
        logger.info(
            f'Добавление валюты: {currency} для пользователя {user_chat_id}'
        )
        for item in self._users_currencies:
            if item['user_id'] == user_chat_id:
                write_currency(currency, item['currencies'])

    def rates_repr(self, user_chat_id: int, amount: str = None) -> str:
        for item in self._users_currencies:
            if (
                item['user_id'] == user_chat_id and
                item['currencies'].ready_for_repr()
            ):
                return show_rates(item['currencies'], amount=amount)
        return no_currencies_chosen(URL)
