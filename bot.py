import logging
import logging.config
import os

from dotenv import load_dotenv
from telegram import InlineKeyboardMarkup, ReplyKeyboardMarkup, Update
from telegram.ext import (ApplicationBuilder, CallbackQueryHandler,
                          CommandHandler, ContextTypes, MessageHandler,
                          filters)

from currencies import UsersIdCurrencies
from untility import POPULAR_CURRENCIES, add_buttons, get_info


load_dotenv()


logging.config.fileConfig('logger.conf')
logger = logging.getLogger(__name__)

user_id_to_currencies = UsersIdCurrencies()


BOT_TOKEN = os.getenv('BOT_TOKEN')

KEYBOARD = [
    ['/add_currency', '/currency_rates'],
    ['/start', '/help'],
    ['/add_amount']
]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Запускает бота и подсказывает детали его интерфейса."""

    user_id_to_currencies.add_user_id(update.effective_chat.id)
    logger.info(
        'Выполнен старт бота для пользователя: '
        f'{update.effective_chat.first_name} - {update.effective_chat.id}'
    )
    text = (
        f'Привет, {update.effective_chat.first_name}!\n'
        'Интересуют актуальные курсы валют?\n\n'
        'Чтобы узнать курс Евро, Доллара США и Болгарского лева к рублю '
        '- нажми \n/currency_rates\n\n'
        'Чтобы узнать курсы других валют нажмите '
        '/add_currency и следуйте подсказкам.'
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        reply_markup=ReplyKeyboardMarkup(KEYBOARD,
                                         resize_keyboard=True))


async def add_currency(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Добавляет валюту к сравнению."""

    reply_markup = InlineKeyboardMarkup(add_buttons())
    user_id_to_currencies.add_user_id(update.effective_chat.id)

    text = ('Выберите БАЗОВУЮ валюту, '
            'относительно которой хотите узнать курс ДРУГИХ валют.\n'
            'Например RUB.\n'
            'Если не знаешь код какой-то валюты, '
            'смело жми /help - там будет подсказка :)')
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=text,
                                   reply_markup=reply_markup)


async def callback_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Парсит коллбэк при выборе валюты."""
    query = update.callback_query
    curr_item = [
        el[-1] for el in enumerate(POPULAR_CURRENCIES)
        if int(query.data) in el
    ]
    user_id_to_currencies.add_currensies_to_user(
        update.effective_chat.id,
        curr_item
    )
    reply_markup = InlineKeyboardMarkup(add_buttons())
    text = ('Выберите ниже валюту, которой хотите узнать курс. '
            'Можно выбрать несколько валют.\n\n'
            'Чтобы узнать курс выбранных валют, '
            'нажмите на кнопку /currency_rates.')
    await query.answer()
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        reply_markup=reply_markup
    )
    supportive_text = ('После выбора валют, можно добавить количество нажав на'
                       ' /add_amount\n'
                       ' я покажу сколько это будет по курсу выбранных валют.')
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=supportive_text)


async def show_currency_rates(update: Update,
                              context: ContextTypes.DEFAULT_TYPE):
    """Показывает курсы выбранных валют."""

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=user_id_to_currencies.rates_repr(update.effective_chat.id)
    )
    text = ('Чтобы узнать курсы других валют нажмите'
            ' /add_currency и следуйте подсказкам.')
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        reply_markup=ReplyKeyboardMarkup(KEYBOARD,
                                         resize_keyboard=True))


async def add_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Добавляет количество конвертируемой валюты к выводу."""

    text = ('В окне чата введите количество валюты,\n'
            'чтобы я показал сколько это будет по курсу выбранных валют.')
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        reply_markup=ReplyKeyboardMarkup(KEYBOARD,
                                         resize_keyboard=True))


async def amount_to_currencies(update: Update,
                               context: ContextTypes.DEFAULT_TYPE):
    """Показывает курсы валют с учетом количества."""

    if not update.message.text.isdigit():
        text = ('Не разобрал :(( Введите количество конвертируемой валюты \n'
                'или нажмите /start для перезагрузки чата.')
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=text)
    else:
        logger.info('Отправка курсов валют пользователю:'
                    f'{update.effective_chat.first_name} - '
                    f'{update.effective_chat.id}')
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=user_id_to_currencies.rates_repr(update.effective_chat.id,
                                                  update.message.text),
            reply_markup=ReplyKeyboardMarkup(KEYBOARD, resize_keyboard=True)
        )


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info('Вызов информации по кодам валют пользователем: '
                f'{update.effective_chat.first_name} - '
                f'{update.effective_chat.id}')
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=get_info(),
        reply_markup=ReplyKeyboardMarkup(KEYBOARD,
                                         resize_keyboard=True))


def main():
    """Запускает бота."""

    application = ApplicationBuilder().token(BOT_TOKEN).build()

    application.add_handlers(
        [
            CommandHandler('start', start),
            CommandHandler('add_currency', add_currency),
            CommandHandler('add_amount', add_amount),
            CommandHandler('currency_rates', show_currency_rates),
            CommandHandler('help', help),
            CallbackQueryHandler(callback_query),
            MessageHandler(filters.TEXT, amount_to_currencies)
        ]
    )

    application.run_polling()


if __name__ == '__main__':
    main()
