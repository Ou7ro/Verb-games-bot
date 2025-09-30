import json
from google.cloud import dialogflow
from environs import env
import argparse


def create_intent(file_name, project_id):
    """Create an intent of the given intent type."""
    with open(file_name, 'r', encoding='utf-8') as questions_file:
        questions = json.load(questions_file)

    for display_name, question_data in questions.items():
        training_phrases_parts = question_data.get('questions', [])
        messages = [question_data.get('answer', '')]

        intents_client = dialogflow.IntentsClient()
        parent = dialogflow.AgentsClient.agent_path(project_id)
        training_phrases = []
        for training_phrases_part in training_phrases_parts:
            part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
            training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
            training_phrases.append(training_phrase)

        text = dialogflow.Intent.Message.Text(text=messages)
        message = dialogflow.Intent.Message(text=text)

        intent = dialogflow.Intent(
            display_name=display_name, training_phrases=training_phrases, messages=[message]
        )

        response = intents_client.create_intent(
            request={"parent": parent, "intent": intent}
        )


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Создание интентов DialogFlow из JSON файла'
    )
    parser.add_argument(
        'file_path',
        help='Путь к JSON файлу с интентами',
    )
    args = parser.parse_args()
    env.read_env()
    project_id = env.str('DIALOGFLOW_PROJECT_ID')
    create_intent(args.file_path, project_id)
