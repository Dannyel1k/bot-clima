import requests
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

TOKEN = "8525579637:AAEsjWlG7WVIPdXDqWG1z4asKEV5S6oktTY"
API_KEY = "c76fbec0e18645652a17c73903e13e49"

# coordenadas (sua região)
LAT = -8.5844
LON = -39.8127

def pegar_clima():
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={LAT}&lon={LON}&appid={API_KEY}&units=metric&lang=pt_br"
    resposta = requests.get(url).json()

    temp = resposta["main"]["temp"]
    sensacao = resposta["main"]["feels_like"]
    umidade = resposta["main"]["humidity"]
    vento = resposta["wind"]["speed"]
    clima = resposta["weather"][0]["description"]

    return f"""
☁️ Clima atual

🌡️ Temperatura: {temp}°C
🥵 Sensação térmica: {sensacao}°C
💧 Umidade: {umidade}%
💨 Vento: {vento} m/s
🌥️ Condição: {clima}
"""

def pegar_previsao():
    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={LAT}&lon={LON}&appid={API_KEY}&units=metric&lang=pt_br"
    resposta = requests.get(url).json()

    previsao = "📅 Previsão próximos dias\n\n"

    for item in resposta["list"][:8]:
        temp = item["main"]["temp"]
        clima = item["weather"][0]["description"]
        hora = item["dt_txt"]

        previsao += f"{hora}\n🌡️ {temp}°C | {clima}\n\n"

    return previsao

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    teclado = ReplyKeyboardMarkup(
        [["clima", "amanha"], ["semana", "chuva"]],
        resize_keyboard=True
    )

    await update.message.reply_text(
        "🌤️ BOT CLIMÁTICO\n\nEscolha uma opção:",
        reply_markup=teclado
    )

async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):

    texto = update.message.text.lower()

    if texto == "clima":
        await update.message.reply_text(pegar_clima())

    elif texto == "amanha":
        await update.message.reply_text(pegar_previsao())

    elif texto == "semana":
        await update.message.reply_text(pegar_previsao())

    elif texto == "chuva":
        await update.message.reply_text(pegar_previsao())

async def main():

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT, responder))

    print("Bot rodando...")

    await app.run_polling()

import asyncio
asyncio.run(main())