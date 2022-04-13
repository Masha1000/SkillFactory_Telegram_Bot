import telebot

from Config import TOKEN, exchanger
from Extensions import Convertor, APIException
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту в следующем формате:\n<Имя валюты> \
     <В какую валюту перевести> \
    < Колличество переводимой валюты>\nУвидеть список всех доступных валют: /values'
    bot.send_message(message.chat.id, text)
@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:\n'
    text += "\n".join(f"{i+1}. {key}" for i, key in enumerate(exchanger.keys()))
    bot.reply_to(message, text)
@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    values = message.text.split( )
    values = list(map(str.lower, values))

    try:
        result = Convertor.get_price(values)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя \n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду \n{e}')
    else:
        text = f'Цена {values[2]} {values[0]} в {values[1]} -- {result}'

        bot.reply_to(message, text)

bot.polling(none_stop=True, interval=0)
