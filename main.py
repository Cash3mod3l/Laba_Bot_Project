import telebot
import requests

bot_token = '6097965316:AAEYvR1BtWrFwZOvzM1xi6uqAK3WtIe8IH0' # Введите свой токен бота
last_fm_api_key = '85b12c020b5eaf3f0ebb442d906431d5' # Введите свой API ключ от Last.fm

bot = telebot.TeleBot(bot_token)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, 'Привет! Введите имя артиста или название альбома, о котором хотите узнать.')

# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
def search_artist_or_album(message):
    query = message.text
    search_url = f'http://ws.audioscrobbler.com/2.0/?method=album.search&album={query}&api_key={last_fm_api_key}&format=json'
    search_result = requests.get(search_url).json()
    albums = search_result['results']['albummatches']['album']
    if len(albums) == 0:
        bot.reply_to(message, 'Не удалось найти информацию об этом артисте или альбоме.')
    else:
        for album in albums[:5]:
            album_name = album['name']
            artist_name = album['artist']
            album_url = album['url']
            reply_text = f'🎵 {artist_name} - {album_name}\n\nТреклист:\n{album_url}'
            bot.send_message(message.chat.id, reply_text)

bot.polling()
