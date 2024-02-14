# подключение библиотек
# В google colab добавить: !pip install wikipedia
# В google colab добавить: !pip install pyTelegramBotAPI

import telebot, wikipedia, re
from telebot import types
import requests
from bs4 import BeautifulSoup

bot = telebot.TeleBot('Your token') #Здесь впиши токен, полученный от @botfather

wikipedia.set_lang("ru")
def getwiki(s):
    try:
        ny = wikipedia.page(s)
        wikitext=ny.content[:1000]
        wikimas=wikitext.split('.')
        wikimas = wikimas[:-1]
        wikitext2 = ''
        for x in wikimas:
            if not('==' in x):
                if(len((x.strip()))>3):
                   wikitext2=wikitext2+x+'.'
            else:
                break
        wikitext2=re.sub('\([^()]*\)', '', wikitext2)
        wikitext2=re.sub('\([^()]*\)', '', wikitext2)
        wikitext2=re.sub('\{[^\{\}]*\}', '', wikitext2)
        return wikitext2
    except Exception as e:
        return 'В энциклопедии нет информации об этом'
@bot.message_handler(commands=["start"])
def welcome(message):
    bot.send_video(message.chat.id, 'https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExOHdxcnJseDc2bW5iejM2OWJxdDRsYWFuZG1tMDl1Ynh4bmM1ZXZucyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/zzxTCSgkHfT1K/giphy.gif', None, 'Text')
    bot.send_message(message.chat.id, "Нужна информация из wiki, {0.first_name}? Просто напиши, что ты хочешь узнать.".format(message.from_user, bot.get_me()),
        parse_mode='html')
    
def get_wiki_image_url(page_name):
    response = requests.get(f"https://ru.wikipedia.org/wiki/{page_name}")
    soup = BeautifulSoup(response.text, 'html.parser')
    images = soup.find_all('img')
    if images:
        return 'https:' + images[0]['src']
    else:
        extension = image_url.split('.')[-1]
    if extension not in ['jpg', 'jpeg', 'png']:
        return None
        bot.send_message(chat_id, "Извините, но я не могу отправить это изображение. Пожалуйста, попробуйте другой запрос.")
    else:
        return image_url is None
        bot.send_message(chat_id, "Извините, но я не могу найти изображение для этого запроса.")

@bot.message_handler(content_types=["text"])
def handle_text(message):
    chat_id = message.chat.id
    image_url = get_wiki_image_url(message.text)
    bot.send_photo(chat_id, photo=image_url)
    bot.send_message(chat_id, getwiki(message.text))


bot.polling(none_stop=True)
