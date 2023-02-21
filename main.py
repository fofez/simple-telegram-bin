# Import the Python Packages
import telebot
import requests

#Change TOKEN for your Bot token given by @BotFather
bot = telebot.TeleBot("TOKEN")

#Start command
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Welcome! To use the bot please send a message like this /bin XXXXXX.")

#BIN Command
@bot.message_handler(func=lambda message: message.text.startswith('/bin ') and message.text[5:].isdigit() and len(message.text[5:]) >= 6 and len(message.text[5:]) <= 8)
def check_bin(message):
    bin_number = message.text[5:]
    response = requests.get("https://lookup.binlist.net/" + bin_number)
    if response.status_code == 200:
        data = response.json()
        formatted_response = f"""
        Number:
            Length: {data['number']['length']}
            Luhn: {'Yes' if data['number']['luhn'] else 'No'}
        Scheme: {data['scheme']}
        Type: {data['type']}
        Brand: {data['brand']}
        Prepaid: {'Yes' if data['prepaid'] else 'No'}
        Country:
            Numeric: {data['country']['numeric']}
            Alpha2: {data['country']['alpha2']}
            Name: {data['country']['name']}
            Emoji: {data['country']['emoji']}
            Currency: {data['country']['currency']}
            Latitude: {data['country']['latitude']}
            Longitude: {data['country']['longitude']}
        Bank:
            Name: {data['bank']['name']}
            URL: {data['bank']['url']}
            Phone: {data['bank']['phone']}
        """
        bot.reply_to(message, formatted_response)
    else:
        bot.reply_to(message, "BIN Checker API is down or server is currently unable to connect.")

#Start Bot
bot.polling()
