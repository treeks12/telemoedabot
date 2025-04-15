# Import base
import requests
import json
import time
import aiohttp


# Import bot
import asyncio

from telebot.async_telebot import AsyncTeleBot



bot_token = ""

bot = AsyncTeleBot(bot_token)

global_usdbrl = 0.0
global_eurbrl = 0.0
global_chfbrl = 0.0
global_gbpbrl = 0.0


@bot.message_handler(commands=["usd"])
async def usd(msg):
    global global_usdbrl

    try:
        valor = msg.text.split()
        valor_reais = float(valor[1])

        resultado = float(valor_reais) / float(global_usdbrl)

        resposta = f"{valor_reais:.2f} R$ é igual a {resultado:.2f} USD"
        await bot.send_message(msg.chat.id, resposta)

    except (ValueError, IndexError):
        await bot.send_message(msg.chat.id, "Use o comando corretamente /usd VALOR")


@bot.message_handler(commands=["eur"])
async def eur(msg):
    global global_eurbrl

    try:
        valor = msg.text.split()
        valor_reais = float(valor[1])

        resultado = float(valor_reais) / float(global_eurbrl)

        resposta = f"{valor_reais:.2f} R$ é igual a {resultado:.2f} EUR"
        await bot.send_message(msg.chat.id, resposta)

    except (ValueError, IndexError):
        await bot.send_message(msg.chat.id, "Use o comando corretamente /eur VALOR")

@bot.message_handler(commands=["chf"])
async def chf(msg):
    global global_chfbrl

    try:
        valor = msg.text.split()
        valor_reais = float(valor[1])

        resultado = float(valor_reais) / float(global_chfbrl)

        resposta = f"{valor_reais:.2f} R$ é igual a {resultado:.2f} CHF"
        await bot.send_message(msg.chat.id, resposta)

    except (ValueError, IndexError):
        await bot.send_message(msg.chat.id, "Use o comando corretamente /chf VALOR")

@bot.message_handler(commands=["gpb"])
async def gbp(msg):
    global global_gbpbrl

    try:
        valor = msg.text.split()
        valor_reais = float(valor[1])

        resultado = float(valor_reais) / float(global_chfbrl)

        resposta = f"{valor_reais:.2f} R$ é igual a {resultado:.2f} GBP"
        await bot.send_message(msg.chat.id, resposta)

    except (ValueError, IndexError):
        await bot.send_message(msg.chat.id, "Use o comando corretamente /gbp VALOR")


async def iniciar(msg):
    return True

@bot.message_handler(func=iniciar)
async def resposta(msg):
    url = requests.get('https://economia.awesomeapi.com.br/last/USD-BRL,EUR-BRL,CHF-BRL,GBP-BRL,BTC-USD,ETH-USD,LTC-USD,SOL-USD,BNB-USD')
    data = url.json()
    global global_usdbrl, global_eurbrl, global_chfbrl, global_gbpbrl

    global_usdbrl = float(data['USDBRL']['bid'])
    global_eurbrl = float(data['EURBRL']['bid'])
    global_chfbrl = float(data['CHFBRL']['bid'])
    global_gbpbrl = float(data['GBPBRL']['bid'])

    txt = (
        "Bem-vindo ao conversor de moedas!\n\n"
        "  Cotações atualizadas:\n"
        f"  - Dólar (USD): R$ {global_usdbrl:.2f}\n"
        f"  - Euro (EUR): R$ {global_eurbrl:.2f}\n"
        f"  - Franco Suiço (CHF): R$ {global_chfbrl:.2f}\n"
        f"  - Libra Esterlina (GBP): R$ {global_gbpbrl:.2f}\n\n"
        "  /valores - Para ver o valor em real de todas as moedas\n"
        "  /usd (valor em real) - Para converter Reais para Dolar\n"
        "  /eur (valor em real) - Para converter Reais para Euro\n"
        "  /chf (valor em real) - Para converter Reais para Franco Suiço\n"
        "  /gbp (valor em real) - Para converter Reais para Libra Esterlina\n"
    )

    await bot.reply_to(msg, txt)

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(bot.polling(non_stop=True))
