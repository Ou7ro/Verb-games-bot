from logger import setup_logger
from environs import env
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from google.cloud import dialogflow
from google.oauth2 import service_account


logger = setup_logger()


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_markdown_v2(
        'Здравствуйте, напишите мне по интересующему вас вопросу',
    )


def handle_message(update: Update, context: CallbackContext):
    user_message = update.message.text
    user_id = update.message.from_user.id
    project_id = env.str('DIALOGFLOW_PROJECT_ID')
    aplication_path = env.str('GOOGLE_APPLICATION_PATH')
    try:
        credentials = service_account.Credentials.from_service_account_file(
            aplication_path,
            scopes=['https://www.googleapis.com/auth/cloud-platform']
        )
        session_client = dialogflow.SessionsClient(credentials=credentials)
        session = session_client.session_path(project_id, user_id)
        text_input = dialogflow.TextInput(text=user_message, language_code='ru')
        query_input = dialogflow.QueryInput(text=text_input)
        response = session_client.detect_intent(
            request={"session": session, "query_input": query_input}
        )
        bot_response = response.query_result.fulfillment_text
        update.message.reply_text(bot_response)
    except Exception as e:
        logger.error(f'Error in Telegram handler: {e}')


def run_telegram_bot():
    logger.info('Запуск Telegram бота')

    tg_bot_token = env.str('TG_BOT_TOKEN')
    try:
        updater = Updater(tg_bot_token)
        dispatcher = updater.dispatcher
        dispatcher.add_handler(CommandHandler("start", start))
        dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
        updater.start_polling()
        updater.idle()
    except Exception as e:
        logger.error(f'Telegram bot error: {e}')


if __name__ == '__main__':
    run_telegram_bot()
