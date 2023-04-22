import telegram
import requests
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

# Токен бота
TOKEN = '6097965316:AAEYvR1BtWrFwZOvzM1xi6uqAK3WtIe8IH0'

# Ключ API Last.fm
LASTFM_API_KEY = '85b12c020b5eaf3f0ebb442d906431d5'

# URL для API Last.fm
LASTFM_API_URL = 'http://ws.audioscrobbler.com/2.0/'


# Функция для обработки команды /start
def start(update, context):
    update.message.reply_text(
        'Привет! Я бот для поиска и предоставления информации о музыкальных артистах и альбомах. Просто отправьте название артиста или альбома, и я вышлю вам информацию о нём.')


# Функция для обработки сообщений с текстом
def search(update, context):
    # Получаем текст сообщения
    query = update.message.text

    # Формируем параметры запроса к API Last.fm
    params = {
        'method': 'album.search',
        'api_key': LASTFM_API_KEY,
        'format': 'json',
        'album': query
    }

    # Отправляем запрос к API Last.fm
    response = requests.get(LASTFM_API_URL, params=params)

    # Получаем данные из ответа в формате JSON
    data = response.json()

    # Получаем первый найденный альбом
    album = data['results']['albummatches']['album'][0]

    # Формируем ответ пользователю
    response_text = f"Название альбома: {album['name']}\n" \
                    f"Исполнитель: {album['artist']}\n" \
                    f"URL: {album['url']}"

    # Отправляем ответ пользователю
    update.message.reply_text(response_text)


# Создаем объект бота и передаем ему токен
bot = telegram.Bot(token=TOKEN)

# Создаем обработчик команды /start
start_handler = CommandHandler('start', start)

# Создаем обработчик текстовых сообщений
search_handler = MessageHandler(Filters.text, search)

# Создаем объект Updater и передаем ему токен и обработчики команд и сообщений
updater = Updater(TOKEN, use_context=True)
updater.dispatcher.add_handler(start_handler)
updater.dispatcher.add_handler(search_handler)

# Запускаем бота
updater.start_polling()


updater.idle()
