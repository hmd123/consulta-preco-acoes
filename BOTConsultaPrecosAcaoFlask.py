from flask import Flask, request
import telebot
import yfinance as yf
import os
import requests

app = Flask(__name__)

# Configuração do Bot
BOT_API_TOKEN = os.getenv('BOT_API_TOKEN')
WEBHOOK_URL = os.getenv('WEBHOOK_URL_TOKEN')

if not BOT_API_TOKEN or not WEBHOOK_URL:
    raise ValueError('BOT_API_TOKEN ou WEBHOOK_URL não estão definidos')

bot = telebot.TeleBot(BOT_API_TOKEN)

# Função para obter o preço da ação
def obter_preco(ticker):
    try:
        acao = yf.Ticker(ticker)
        preco_atual = acao.history(period='1d')['Close'].iloc[-1]
        preco_atual = f"{preco_atual:.2f}"
        return preco_atual
    except Exception as e:
        log_erro = f"Não foi possível buscar a ação. Erro: {str(e)}"
        return log_erro

# Endpoint que o Telegram chamará
@app.route(f'/{BOT_API_TOKEN}', methods=['POST'])
def webhook():
    update = request.get_json()
    try:
        bot.process_new_updates([telebot.types.Update.de_json(update)])
    except Exception as e:
        print(f"Erro ao processar o update: {e}")
    return '', 200

# Configura o webhook do bot
def set_webhook():
    webhook_url = f'https://api.telegram.org/bot{BOT_API_TOKEN}/setWebhook?url={WEBHOOK_URL}'
    response = requests.get(webhook_url)
    if response.status_code == 200:
        print('Webhook configurado com sucesso!')
    else:
        print('Falha ao configurar webhook.')

# Endpoint para configuração do webhook
@app.route('/set_webhook', methods=['GET'])
def configure_webhook():
    set_webhook()
    return 'Webhook configurado', 200

# Configura os handlers de mensagens
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Olá! Digite o código da ação que deseja consultar.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    acao = message.text.upper() + ".SA"
    preco_info = obter_preco(acao)
    bot.reply_to(message, preco_info)

# Inicia o servidor Flask e configura o webhook
if __name__ == '__main__':
    set_webhook()  # Configure o webhook ao iniciar
    app.run(host='0.0.0.0', port=8080)
