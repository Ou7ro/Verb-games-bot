from vk_api.longpoll import VkLongPoll, VkEventType
from logger import setup_logger
import random
from environs import env
import vk_api as vk
from google.cloud import dialogflow
from google.oauth2 import service_account
import logging


logger = logging.getLogger(__name__)


def handle_message(event, vk_api, project_id, aplication_path):
    try:
        credentials = service_account.Credentials.from_service_account_file(
            aplication_path,
            scopes=['https://www.googleapis.com/auth/cloud-platform']
        )
        session_client = dialogflow.SessionsClient(credentials=credentials)

        session = session_client.session_path(project_id, event.user_id)

        text_input = dialogflow.TextInput(text=event.text, language_code='ru')
        query_input = dialogflow.QueryInput(text=text_input)
        response = session_client.detect_intent(
            request={"session": session, "query_input": query_input}
        )
        bot_response = response.query_result.fulfillment_text
        if not response.query_result.intent.is_fallback:
            vk_api.messages.send(
                user_id=event.user_id,
                message=bot_response,
                random_id=random.randint(1,1000)
            )
    except Exception as e:
        logger.error(f"Error in VK handler: {e}")


def run_vk_bot():
    setup_logger()
    logger.info('Запуск VK бота')
    vk_token = env.str('VK_TOKEN_BOT')
    project_id = env.str('DIALOGFLOW_PROJECT_ID')
    aplication_path = env.str('GOOGLE_APPLICATION_PATH')

    vk_session = vk.VkApi(token=vk_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    try:
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                handle_message(event, vk_api, project_id, aplication_path)
    except Exception as e:
        logger.error(f"VK bot error: {e}")


def main():
    env.read_env()
    run_vk_bot()


if __name__ == "__main__":
    main()
