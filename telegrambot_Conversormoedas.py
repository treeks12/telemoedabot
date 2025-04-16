# Import base
import requests
import json
import time
import aiohttp

# Import bot
import asyncio
from telebot.async_telebot import AsyncTeleBot

# Token do bot
bot_token = "7911138635:AAEzYdp9tm0yA2ObIVZDDXG_y7zmx4cqFaY"
bot = AsyncTeleBot(bot_token)

# Dicionário global para armazenar cotações
global_cotacoes = {}

# Lista de moedas suportadas
MOEDAS = [
    "usd", "eur", "chf", "gbp", "aed", "ars", "aud", "bnb", "bob", "brett",
    "btc", "cad", "clp", "cny", "cop", "crc", "czk", "dkk", "doge", "egp",
    "eth", "huf", "hkd", "inr", "ils", "jpy", "kes", "krw", "ltc", "mxn",
    "nok", "nzd", "pen", "php", "pln", "pyg", "ron", "rsd", "rub", "sar",
    "sgd", "sol", "thb", "try", "twd", "uyu", "vef", "xag", "xau", "xrp", "zar"
]

# Lista de comandos para conversão contrária (ex.: usdtobrl)
MOEDAS_TO_BRL = [f"{moeda}tobrl" for moeda in MOEDAS]

# Função de conversão genérica (BRL para moeda)
@bot.message_handler(commands=MOEDAS)
async def converter_moeda(msg):
    try:
        # Extrair o comando (ex.: "usd" de "/usd")
        comando = msg.text.split()[0][1:].lower()
        valor_reais = float(msg.text.split()[1])

        # Verificar se a moeda existe no dicionário
        if comando.upper() not in global_cotacoes:
            raise ValueError("Cotação não disponível")

        cotacao = global_cotacoes[comando.upper()]
        resultado = valor_reais / cotacao
        resposta = f"{valor_reais:.2f} R$ é igual a {resultado:.2f} {comando.upper()}"
        await bot.send_message(msg.chat.id, resposta)
    except (ValueError, IndexError):
        await bot.send_message(msg.chat.id, f"Use o comando corretamente /{comando} VALOR")

# Função de conversão contrária (moeda para BRL)
@bot.message_handler(commands=MOEDAS_TO_BRL)
async def converter_para_brl(msg):
    try:
        # Extrair o comando (ex.: "usd" de "/usdtobrl")
        comando = msg.text.split()[0][1:].lower().replace("tobrl", "")
        valor_moeda = float(msg.text.split()[1])

        # Verificar se a moeda existe no dicionário
        if comando.upper() not in global_cotacoes:
            raise ValueError("Cotação não disponível")

        cotacao = global_cotacoes[comando.upper()]
        resultado = valor_moeda * cotacao
        resposta = f"{valor_moeda:.2f} {comando.upper()} é igual a {resultado:.2f} R$"
        await bot.send_message(msg.chat.id, resposta)
    except (ValueError, IndexError):
        await bot.send_message(msg.chat.id, f"Use o comando corretamente /{comando}tobrl VALOR")

# Comando /lista
@bot.message_handler(commands=["lista"])
async def lista(msg):
    txt = "Moedas disponíveis e seus preços em R$:\n\n"
    for moeda in MOEDAS:
        nome_moeda = {
            "usd": "Dólar Americano",
            "eur": "Euro",
            "chf": "Franco Suíço",
            "gbp": "Libra Esterlina",
            "aed": "Dirham dos Emirados",
            "ars": "Peso Argentino",
            "aud": "Dólar Australiano",
            "bnb": "Binance Coin",
            "bob": "Boliviano",
            "brett": "Brett",
            "btc": "Bitcoin",
            "cad": "Dólar Canadense",
            "clp": "Peso Chileno",
            "cny": "Yuan Chinês",
            "cop": "Peso Colombiano",
            "crc": "Colón Costarriquenho",
            "czk": "Coroa Checa",
            "dkk": "Coroa Dinamarquesa",
            "doge": "Dogecoin",
            "egp": "Libra Egípcia",
            "eth": "Ethereum",
            "huf": "Florim Húngaro",
            "hkd": "Dólar de Hong Kong",
            "inr": "Rúpia Indiana",
            "ils": "Novo Shekel Israelense",
            "jpy": "Iene Japonês",
            "kes": "Shilling Queniano",
            "krw": "Won Sul-Coreano",
            "ltc": "Litecoin",
            "mxn": "Peso Mexicano",
            "nok": "Coroa Norueguesa",
            "nzd": "Dólar Neozelandês",
            "pen": "Sol do Peru",
            "php": "Peso Filipino",
            "pln": "Zlóti Polonês",
            "pyg": "Guarani Paraguaio",
            "ron": "Leu Romeno",
            "rsd": "Dinar Sérvio",
            "rub": "Rublo Russo",
            "sar": "Riyal Saudita",
            "sgd": "Dólar de Cingapura",
            "sol": "Solana",
            "thb": "Baht Tailandês",
            "try": "Nova Lira Turca",
            "twd": "Dólar Taiuanês",
            "uyu": "Peso Uruguaio",
            "vef": "Bolívar Venezuelano",
            "xag": "Prata Spot",
            "xau": "Ouro",
            "xrp": "XRP",
            "zar": "Rand Sul-Africano"
        }.get(moeda, moeda.upper())
        txt += f" - {nome_moeda} ({moeda.upper()}): R$ {global_cotacoes.get(moeda.upper(), 0.0):.2f}\n"
    await bot.send_message(msg.chat.id, txt)

# Mensagem de boas-vindas
async def iniciar(msg):
    return True

@bot.message_handler(func=iniciar)
async def resposta(msg):
    txt = (
        "Bem-vindo RealGlobal! - Seu conversor de moedas para Real (BRL)\n\n"
        "  Cotações atualizadas:\n"
        f"  - Dólar (USD): R$ {global_cotacoes.get('USD', 0.0):.2f}\n"
        f"  - Euro (EUR): R$ {global_cotacoes.get('EUR', 0.0):.2f}\n"
        f"  - Franco Suiço (CHF): R$ {global_cotacoes.get('CHF', 0.0):.2f}\n"
        f"  - Libra Esterlina (GBP): R$ {global_cotacoes.get('GBP', 0.0):.2f}\n\n"
        "Use os comandos para converter moedas:\n\n"
        "  /lista - Para ver todas as moedas disponíveis (50 moedas dísponiveis)\n\n"
        "Converter de BRL para outra moeda:\n"
        "  /usd (valor em real) - Ex.: /usd 100 para converter 100 BRL para USD\n"
        "  /eur (valor em real) - Ex.: /eur 100 para converter 100 BRL para EUR\n"
        "  /chf (valor em real) - Ex.: /chf 100 para converter 100 BRL para CHF\n"
        "  /gbp (valor em real) - Ex.: /gbp 100 para converter 100 BRL para GBP\n\n"
        "Converter de outra moeda para BRL:\n"
        "  /usdtobrl (valor em USD) - Ex.: /usdtobrl 100 para converter 100 USD para BRL\n"
        "  /eurtobrl (valor em EUR) - Ex.: /eurtobrl 100 para converter 100 EUR para BRL\n"
        "  /chftobrl (valor em CHF) - Ex.: /chftobrl 100 para converter 100 CHF para BRL\n"
        "  /gbptobrl (valor em GBP) - Ex.: /gbptobrl 100 para converter 100 GBP para BRL\n"
    )
    await bot.reply_to(msg, txt)

# Função para atualizar cotações
async def loop_api():
    global global_cotacoes
    moedas_api = ",".join(f"{moeda.upper()}-BRL" for moeda in MOEDAS)

    while True:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f'https://economia.awesomeapi.com.br/last/{moedas_api}') as asyncdata:
                    data = await asyncdata.json()

                    # Atualizar cotações no dicionário
                    for moeda in MOEDAS:
                        chave = f"{moeda.upper()}BRL"
                        if chave in data:
                            global_cotacoes[moeda.upper()] = float(data[chave]['bid'])

                    print(
                        f"Cotações atualizadas: {', '.join(f'{moeda.upper()}: {global_cotacoes.get(moeda.upper(), 0.0):.2f}' for moeda in MOEDAS)}")

        except Exception as e:
            print(f"Erro ao atualizar cotações: {e}")

        await asyncio.sleep(30)

# Função principal
async def main():
    await asyncio.gather(bot.polling(non_stop=True), loop_api())

asyncio.run(main())
