import telebot
from config import TOKEN
from extensions import CurrencyConverter, APIException

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    text = (
        "Добро пожаловать в Конвертер валют!\n"
        "Чтобы получить курс валют, введите команду в формате:\n"
        "<имя валюты> <валюта для конвертации> <количество>\n"
        "Например: USD EUR 10\n"
        "Доступные валюты: USD, EUR, RUB, BYN, CNY, AED, HKD, TRY\n"
        "Команда /values покажет все доступные валюты."
    )
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message):
    text = "Доступные валюты:\nUSD - Доллар США\nEUR - Евро\nRUB - Российский рубль\nBYN - Белорусский рубль\nCNY - Юань\nAED - ОАЭ дирхам\nHKD - Гонконгский доллар\nTRY - Турецкая лира"
    bot.reply_to(message, text)

@bot.message_handler(func=lambda message: True)
def convert_currency(message):
    try:
        values = message.text.split()
        if len(values) != 3:
            raise APIException('Неверное количество параметров. Используйте формат: <валюта> <валюта для конвертации> <количество>.')

        base, quote, amount = values
        total_amount = CurrencyConverter.get_price(base.upper(), quote.upper(), amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка: {str(e)}')
    except Exception as e:
        bot.reply_to(message, f'Неизвестная ошибка: {str(e)}')
    else:
        text = f'{amount} {base.upper()} равняется {total_amount:.2f} {quote.upper()}'
        bot.send_message(message.chat.id, text)

if __name__ == '__main__':
    bot.polling(none_stop=True)