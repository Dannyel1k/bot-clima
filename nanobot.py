import requests
from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "8525579637:AAEsjWlG7WVIPdXDqWG1z4asKEV5S6oktTY"
API_KEY = "c76fbec0e18645652a17c73903e13e49"

cidade = "Santa Maria da Boa Vista,BR"

async def clima(update: Update, context: ContextTypes.DEFAULT_TYPE):

    url = f"https://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={API_KEY}&units=metric&lang=pt_br"

    dados = requests.get(url).json()

    temp = dados["main"]["temp"]
    sensacao = dados["main"]["feels_like"]
    umidade = dados["main"]["humidity"]
    vento = dados["wind"]["speed"]
    clima = dados["weather"][0]["description"]

    nascer = dados["sys"]["sunrise"]
    por = dados["sys"]["sunset"]
    timezone = dados["timezone"]

    nascer_sol = datetime.utcfromtimestamp(nascer) + timedelta(seconds=timezone)
    por_sol = datetime.utcfromtimestamp(por) + timedelta(seconds=timezone)

    nascer_formatado = nascer_sol.strftime("%H:%M")
    por_formatado = por_sol.strftime("%H:%M")

    resposta = f"""
☀️ Clima em Santa Maria da Boa Vista

🌡️ Temperatura: {temp:.2f}°C
🥵 Sensação térmica: {sensacao:.2f}°C
💧 Umidade: {umidade}%
💨 Vento: {vento} m/s
🌥️ Condição: {clima}

🌅 Nascer do sol: {nascer_formatado}
🌇 Pôr do sol: {por_formatado}
"""

    await update.message.reply_text(resposta)

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("clima", clima))

print("BOT CLIMA ONLINE")

app.run_polling()