# Verb-games-bot

Проект включает двух ботов (для Telegram и VK), которые используют DialogFlow для обработки естественного языка и ответов на вопросы пользователей. Также предоставлен скрипт для обучения DialogFlow интентами из JSON-файла.

## Примеры работающих ботов
@verbik_game_bot - телеграм бот

https://vk.com/club232796651 - группа с вк ботом.

Доступные темы для сообщений:

`Где проходит совещание?`
`Как удалить аккаунт?`
`Как устроиться к вам?`
`Не помню пароль?`

И разлиные формулироваки вопросов на данные темы.

## Зависимости

- Python3.7=< должен быть уже установлен
- Затем используйте `pip` для установки зависимостей:

```bash
pip install -r requirements.txt
```

## Переменные окружения
Создайте и настройте файл .env:

```
TG_BOT_TOKEN=199999999:QWEtryhdj_Fjdfyeu...   # Токен для телеграм-бота
TG_BOT_LOGER=199999999:QWEtryhdj_Fjdfyeu...   # Токен телеграм-бота для логирования
VK_TOKEN_BOT=vk1.a.:RLGKRLEVNHJKERVOKNMEV...  # Ключи доступа от сообщества в ВК
DIALOGFLOW_PROJECT_ID=your_project_id         # ID проекта Dialogflow
GOOGLE_APPLICATION_PATH=./credentials.json    # Путь к файлу сервисного ключа Dialogflow
TG_CHAT_ID=123456789                          # ID вашего Телеграм-чата, в который бот будет дублировать логи с ошибками
```

## Запуск

1. Склонируйте репозиторий на свое устройство `git clone https://github.com/Ou7ro/Verb-games-bot.git`

2. Установите зависимости `pip install -r requirements.txt`

3. Создайте проект в [Google Cloud](https://console.cloud.google.com/welcome?project=newagent-prhm)

4. Включите [Dialogflow API](https://console.cloud.google.com/apis/enableflow?apiid=dialogflow.googleapis.com)

5. Создайте агента Dialogflow ES

6. Создайте сервисный аккаунт и скачайте [credentials.json](https://console.cloud.google.com/projectselector2/iam-admin/serviceaccounts?supportedpurview=project)

7. Создайте базовые интенты с помощью скрипта dialog_flow_learning, либо вручную c помощью файла `learning_script.py`, его работа будет описана ниже.

8. Создайте сообщество в вк, после чего всключите бота в сообществе.

9. В сообществе создайте ключи доступа

10. Создайте телеграм бота и получите его токен.

11. Настройте переменные окружения

12. Запустите нужного бота:

Telegram-бот:
```bash
python tg_handler.py
```

VK-бот:
```bash
python vk_handler.py
```

### Обучение DialogFlow

Скрипт `learning_script.py` предназначен для создания интентов в DialogFlow из JSON-файла с вопросами и ответами.

#### Использование

```bash
python learning_script.py путь/к/файлу.json
```

#### Структура JSON-файла

```json
{
  "Устройство на работу": {
    "questions": [
      "Как устроиться к вам на работу?",
      "Как устроиться к вам?",
      "Возможность трудоустройства",
      "Хочу работать у вас"
    ],
    "answer": "Если вы хотите работать в нашей компании, отправьте резюме на email: hr@company.com"
  },
  "Часы работы": {
    "questions": [
      "Когда вы работаете?",
      "Режим работы",
      "Часы работы офиса",
      "Во сколько открываетесь?"
    ],
    "answer": "Мы работаем с понедельника по пятницу с 9:00 до 18:00"
  }
}
```

После выполнения скрипта интенты появятся в вашем агенте DialogFlow и будут доступны для использования ботами.

### Пример работы

![Пример использования ТГ Бота](https://github.com/user-attachments/assets/3cdd2e16-595d-47ef-be6d-cd7ef0e3c572)

![Пример использования ВК бота](https://github.com/user-attachments/assets/575da44b-aefd-4b6f-b851-73e4c6d40071)

