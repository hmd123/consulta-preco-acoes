#exporta cÓdigo do botfather
#BOT_API_TOKEN="INSERIR O TOKEN"
import os
import telebot
import yfinance as yf

#bot = telebot.TeleBot(BOT_API_TOKEN)
BOT_API_TOKEN = os.getenv('BOT_API_TOKEN')
print(f"Token: '{BOT_API_TOKEN}'")  # Apenas para depuração

if BOT_API_TOKEN is None:
    raise ValueError('BOT_API_TOKEN não está definido')

def obter_preco(ticker):
    try:
        acao = yf.Ticker(ticker)
        preco_atual = acao.history(period='1d')['Close'].iloc[-1]
        preco_atual = f"{preco_atual:.2f}"
        return preco_atual
    except:
        log_erro = "Não foi possivel buscar Ação. Pode ter acontecido um erro ou a ação foi digitada incorretamente"
        return log_erro

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Olá! Digite o código da ação que deseja consultar.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    acao = message.text.upper()
    acao = symbol+".SA"
    preco_info = obter_preco(acao)
    bot.reply_to(message, preco_info)

# Inicia o bot
bot.polling()
