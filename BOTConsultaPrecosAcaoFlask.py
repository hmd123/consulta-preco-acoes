from flask import Flask
import telebot
import os

app = Flask(__name__)

# Configuração do bot
BOT_API_TOKEN = os.getenv('BOT_API_TOKEN')
bot = telebot.TeleBot(BOT_API_TOKEN)

@app.route('/')
def index():
    return 'Bot está rodando'

@app.route('/webhook', methods=['POST'])
def webhook():
    json_str = request.get_data(as_text=True)
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return '', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
