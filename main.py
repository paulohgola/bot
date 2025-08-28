import os
import telebot
from dotenv import load_dotenv
from grafico import gerar_grafico # Montagem do Gráfico
from comandos import registrar_comandos # Comandos
from db import criar_banco  # Banco de Dados

criar_banco()

load_dotenv()

API_TOKEN = os.environ['API_TOKEN']

bot = telebot.TeleBot(API_TOKEN)


# Dados específicos de cada usuário
user_data = {}

# Lista das despesas de cada usuário
despesas = []

# Registra todos os comandos do bot
registrar_comandos(bot, user_data, despesas, gerar_grafico)

bot.infinity_polling()