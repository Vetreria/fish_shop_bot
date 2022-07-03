import os
import logging
import redis
import dotenv
from telegram import Update, Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Filters, Updater
from telegram.ext import CallbackQueryHandler, CommandHandler, MessageHandler, CallbackContext


from main import fetch_api_token, get_products


_database = None


def make_keyboard():
    keyboard = []
    products = get_products(ep_api_token)
    for product in products:
        keyboard.append([InlineKeyboardButton(product['name'],
                                              callback_data=product['id'])])
    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup


def start(bot, update):
    update.message.reply_text('Каталог:', reply_markup=make_keyboard())
    return "ECHO"


def echo(bot, update):
    users_reply = update.message.text
    update.message.reply_text(users_reply)
    return "ECHO"


def handle_users_reply(update, bot ):
    db = get_database_connection()
    if update.message:
        user_reply = update.message.text
        chat_id = update.message.chat_id
    elif update.callback_query:
        user_reply = update.callback_query.data
        chat_id = update.callback_query.message.chat_id
    else:
        return
    if user_reply == '/start':
        user_state = 'START'
    else:
        user_state = db.get(chat_id).decode("utf-8")
    
    states_functions = {
        'START': start,
        'ECHO': echo
    }
    state_handler = states_functions[user_state]
    # Если вы вдруг не заметите, что python-telegram-bot перехватывает ошибки.
    # Оставляю этот try...except, чтобы код не падал молча.
    # Этот фрагмент можно переписать.
    try:
        next_state = state_handler(bot, update)
        db.set(chat_id, next_state)
    except Exception as err:
        print(err)

def get_database_connection():
    global _database
    if _database is None:
        database_password = os.getenv("DATABASE_PASSWORD")
        database_host = os.getenv("DATABASE_HOST")
        database_port = os.getenv("DATABASE_PORT")
        _database = redis.Redis(host=database_host, port=database_port, password=database_password)
    return _database


if __name__ == '__main__':
    dotenv.load_dotenv()
    token = os.getenv("TELEGRAM_TOKEN")
    ep_store = os.environ["ELASTIC_STORE_ID"]
    ep_client = os.environ["ELASTIC_CLIENT_ID"]
    ep_secret = os.environ["ELASTIC_CLIENT_SECRET"]
    ep_api_token_result = fetch_api_token(ep_client, ep_secret)
    ep_api_token = f"{ep_api_token_result['token_type']} {ep_api_token_result['access_token']}"
    updater = Updater(token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CallbackQueryHandler(handle_users_reply))
    dispatcher.add_handler(MessageHandler(Filters.text, handle_users_reply))
    dispatcher.add_handler(CommandHandler('start', handle_users_reply))
    updater.start_polling()