from vk_api.longpoll import VkLongPoll, VkEventType
from environs import env
import random
import vk_api as vk
from google.cloud import dialogflow
from google.oauth2 import service_account


def echo(event, vk_api):
    vk_api.messages.send(
        user_id=event.user_id,
        message=event.text,
        random_id=random.randint(1,1000)
    )


def handle_message(event, vk_api):
    project_id = env.str('DIALOGFLOW_PROJECT_ID')

    try:
        credentials = service_account.Credentials.from_service_account_file(
            'credentials.json',
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
        pass


if __name__ == "__main__":
    env.read_env()
    vk_token = env.str('VK_TOKEN_BOT')
    vk_session = vk.VkApi(token=vk_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            handle_message(event, vk_api)
