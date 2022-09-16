import logging
import telegram


class TelegramLogsHandler(logging.Handler):

    def __init__(self, log_tg_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = log_tg_bot
        self.tg_bot.send_message(chat_id=self.chat_id, text='LOG-BOT: started')

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


def set_logger(logger, log_tg_bot, chat_id):
    logger_bot = telegram.Bot(token=log_tg_bot)
    logger.setLevel(logging.INFO)
    logger.addHandler(TelegramLogsHandler(logger_bot, chat_id))