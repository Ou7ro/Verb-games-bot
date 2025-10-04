import logging
from telegram import Bot
from environs import env


class TelegramLogsHandler(logging.Handler):
    def __init__(self, tg_token: str, tg_chat_id: str):
        super().__init__()
        self.tg_bot = Bot(token=tg_token)
        self.tg_chat_id = tg_chat_id

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.tg_chat_id, text=log_entry)


def setup_logger():

    env.read_env()

    logger = logging.getLogger(__name__)

    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    try:
        tg_log_token = env.str('TG_BOT_LOGER')
        tg_chat_id = env.str('TG_CHAT_ID')
        telegram_handler = TelegramLogsHandler(tg_log_token, tg_chat_id)
        telegram_handler.setFormatter(logging.Formatter('%(levelname)s\n%(message)s'))
        logger.addHandler(telegram_handler)
    except Exception as e:
        logger.error(f'Не удалось подключить Telegram-логгер: {e}')

    return logger
