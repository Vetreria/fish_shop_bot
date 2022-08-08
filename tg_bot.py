import os
import logging
import redis
import dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler, CommandHandler, MessageHandler, CallbackContext, Filters, Updater


from main import fetch_api_token, get_products, get_product, get_image_url, add_to_cart, get_cart


_database = None


def make_keyboard():
    keyboard = []
    products = get_products(ep_api_token)
    for product in products:
        keyboard.append([InlineKeyboardButton(product['name'],
                                              callback_data=product['id'])])
    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup


def start(update, context):
    update.message.reply_text('Каталог:', reply_markup=make_keyboard())
    return "HANDLE_MENU"


def handle_description(update, context):
    query = update.callback_query

    if query.data == 'back_to_menu':
        context.bot.send_message(
            text='Каталог:',
            chat_id=query.message.chat_id,
            reply_markup=make_keyboard(),
        )
        context.bot.delete_message(
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
        )
        return 'HANDLE_MENU'
    else:
        quantity, item_id = query.data.split('|')
        # print(quantity, item_id)
        cart_id = query.message.chat.id
        add_to_cart(ep_api_token, item_id, quantity, cart_id)
        return 'HANDLE_DESCRIPTION'


def handle_menu(update, context):
    query = update.callback_query
    product = get_product(ep_api_token, query.data)
    text = f"""Карточка товара: {product['name']}
        Описание: {product['description']}
        Цена: {product['meta']['display_price']['with_tax']['formatted']}
        Наличие: {product['meta']['stock']['level']} шт.
        """
    image_id = product['relationships']['main_image']['data']['id']
    keyboard = [ 
        [InlineKeyboardButton('1 шт', callback_data=f'1|{query.data}'),
         InlineKeyboardButton('5 шт', callback_data=f'5|{query.data}'),
         InlineKeyboardButton('10 шт', callback_data=f'10|{query.data}')],
        [InlineKeyboardButton('Назад', callback_data='back_to_menu'),
        InlineKeyboardButton('Корзина', callback_data='cart')
        ]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    image_url = get_image_url(ep_api_token, image_id)
    context.bot.send_photo(
            chat_id=query.message.chat_id,
            photo=image_url, caption = text,
            reply_markup=reply_markup
    )
    
    context.bot.delete_message(chat_id=query.message.chat_id,
                           message_id=query.message.message_id)
    return "HANDLE_DESCRIPTION"


def handle_users_reply(update, context):
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
        'HANDLE_MENU': handle_menu,
        'HANDLE_DESCRIPTION': handle_description
    }
    state_handler = states_functions[user_state]
    # Если вы вдруг не заметите, что python-telegram-bot перехватывает ошибки.
    # Оставляю этот try...except, чтобы код не падал молча.
    # Этот фрагмент можно переписать.
    try:
        next_state = state_handler(update, context)
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