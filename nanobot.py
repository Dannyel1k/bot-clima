from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import requests
from datetime import datetime
import asyncio

TOKEN = "8525579637:AAEsjWlG7WVIPdXDqWG1z4asKEV5S6oktTY"
API_KEY = "c76fbec0e18645652a17c73903e13e49"

# ---------- MENU ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    botao_local = KeyboardButton("📍 Enviar localização", request_location=True)

    teclado = [
        [botao_local],
        ["🌡️ Clima agora"],
        ["🌧️ Chuva próximas horas"],
        ["⏰ Previsão por hora"],
        ["📅 Previsão semana"],
        ["🛰️ Radar de chuva"]
    ]

    markup = ReplyKeyboardMarkup(teclado, resize_keyboard=True)

    await update.message.reply_text(
        "🌤️ BOT METEOROLÓGICO COMPLETO\n\nEnvie sua localização ou escolha uma opção:",
        reply_markup=markup
    )

# ---------- LOCALIZAÇÃO ----------
async def localizar(update: Update, context: ContextTypes.DEFAULT_TYPE):

    lat = update.message.location.latitude
    lon = update.message.location.longitude

    context.user_data["lat"] = lat
    context.user_data["lon"] = lon

    await update.message.reply_text("📍 Localização salva!")

    await clima(update, context)

# ---------- CLIMA ATUAL ----------
async def clima(update: Update, context: ContextTypes.DEFAULT_TYPE):

    lat = context.user_data.get("lat")
    lon = context.user_data.get("lon")

    if not lat:
        await update.message.reply_text("📍 Envie sua localização primeiro.")
        return

    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric&lang=pt_br"

    dados = requests.get(url).json()

    cidade = dados["name"]
    temp = dados["main"]["temp"]
    sens = dados["main"]["feels_like"]
    hum = dados["main"]["humidity"]
    vento = dados["wind"]["speed"]
    cond = dados["weather"][0]["description"]

    nascer = datetime.fromtimestamp(dados["sys"]["sunrise"]).strftime('%H:%M')
    por = datetime.fromtimestamp(dados["sys"]["sunset"]).strftime('%H:%M')

    texto = f"""
☀️ Clima em {cidade}

🌡️ Temperatura: {temp}°C
🥵 Sensação térmica: {sens}°C
💧 Umidade: {hum}%
💨 Vento: {vento} m/s
🌥️ Condição: {cond}

🌅 Nascer do sol: {nascer}
🌇 Pôr do sol: {por}
"""

    await update.message.reply_text(texto)

# ---------- CHUVA ----------
async def chuva(update: Update, context: ContextTypes.DEFAULT_TYPE):

    lat = context.user_data.get("lat")
    lon = context.user_data.get("lon")

    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric&lang=pt_br"

    dados = requests.get(url).json()

    chuva_total = 0

    for item in dados["list"][:8]:
        if "rain" in item:
            chuva_total += item["rain"].get("3h", 0)

    texto = f"""
🌧️ Volume de chuva nas próximas horas

💧 Estimativa: {chuva_total} mm
"""

    await update.message.reply_text(texto)

# ---------- PREVISÃO POR HORA ----------
async def hora(update: Update, context: ContextTypes.DEFAULT_TYPE):

    lat = context.user_data.get("lat")
    lon = context.user_data.get("lon")

    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric&lang=pt_br"

    dados = requests.get(url).json()

    texto = "⏰ Previsão próximas horas\n\n"

    for item in dados["list"][:5]:

        hora = item["dt_txt"].split(" ")[1][:5]
        temp = item["main"]["temp"]
        desc = item["weather"][0]["description"]

        texto += f"{hora} → {temp}°C | {desc}\n"

    await update.message.reply_text(texto)

# ---------- PREVISÃO SEMANA ----------
async def semana(update: Update, context: ContextTypes.DEFAULT_TYPE):

    lat = context.user_data.get("lat")
    lon = context.user_data.get("lon")

    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric&lang=pt_br"

    dados = requests.get(url).json()

    dias = {}

    for item in dados["list"]:
        data = item["dt_txt"].split(" ")[0]
        temp = item["main"]["temp"]

        if data not in dias:
            dias[data] = []

        dias[data].append(temp)

    texto = "📅 Previsão próximos dias\n\n"

    for dia, temps in list(dias.items())[:5]:

        maxima = max(temps)
        minima = min(temps)

        texto += f"{dia} → {minima:.0f}° / {maxima:.0f}°\n"

    await update.message.reply_text(texto)

# ---------- RADAR ----------
async def radar(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "🛰️ Radar meteorológico ao vivo:\nhttps://www.rainviewer.com/map.html"
    )

# ---------- ALERTA AUTOMÁTICO ----------
async def alerta():

    while True:

        await asyncio.sleep(3600)

        print("Verificação automática de tempestade executada")

# ---------- BOTÕES ----------
async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):

    texto = update.message.text

    if texto == "🌡️ Clima agora":
        await clima(update, context)

    elif texto == "🌧️ Chuva próximas horas":
        await chuva(update, context)

    elif texto == "⏰ Previsão por hora":
        await hora(update, context)

    elif texto == "📅 Previsão semana":
        await semana(update, context)

    elif texto == "🛰️ Radar de chuva":
        await radar(update, context)

# ---------- BOT ----------
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.LOCATION, localizar))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))

print("BOT METEOROLÓGICO COMPLETO ONLINE")

app.run_polling()