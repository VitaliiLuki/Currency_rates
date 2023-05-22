from telegram import InlineKeyboardButton

from currencies import COMMON_CURRENCIES


POPULAR_CURRENCIES = ['USD', 'EUR', 'BGN', 'RUB', 'UAH', 'JPY', 'TRY', 'GBP',
                      'CAD', 'CHF', 'CNY', 'INR', 'PLN', 'THB', 'MXN']


def add_buttons():
    """Создает список валют и данных для обратного вызова."""

    buttons = [
        InlineKeyboardButton(text=currency, callback_data=callback)
        for callback, currency in enumerate(POPULAR_CURRENCIES)
        ]
    return [buttons[i:(i+3)] for i in range(0, len(buttons), 3)]


def get_info():
    """Показывает информацию о кодах валют."""

    currencies_codes_info = [
        f'{key} - {value}' for key, value in COMMON_CURRENCIES.items()
        if key in POPULAR_CURRENCIES
    ]
    return '\n'.join(currencies_codes_info)
