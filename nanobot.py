import requests
from datetime import datetime, timedelta
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = "8525579637:AAEsjWlG7WVIPdXDqWG1z4asKEV5S6oktTY"
API_KEY = "c76fbec0e18645652a17c73903e13e49"

menu = [
    [KeyboardButton("📍 Enviar localização", request_location=True)],
    ["🌡 Clima agora"],
    ["🌧 Chuva próximas horas"],
    ["📅 Previsão semana"],
    ["🛰 Radar de chuva"]
]

markup = ReplyKeyboardMarkup(menu, resize_keyboard=True)

usuarios = {}

# START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌤 BOT DO CLIMA\nEnvie sua localização para receber alertas de chuva.",
        reply_markup=markup
    )

# RECEBER LOCALIZAÇÃO
async def receber_localizacao(update: Update, context: ContextTypes.DEFAULT_TYPE):

    lat = update.message.location.latitude
    lon = update.message.location.longitude
    chat_id = update.message.chat_id

    usuarios[chat_id] = {"lat": lat, "lon": lon}

    await update.message.reply_text("📍 Localização salva! Alertas ativados.")

# CLIMA AGORA
async def clima(update: Update, context: ContextTypes.DEFAULT_TYPE):

    chat_id = update.message.chat_id

    if chat_id not in usuarios:
        await update.message.reply_text("📍 Envie sua localização primeiro.")
        return

    lat = usuarios[chat_id]["lat"]
    lon = usuarios[chat_id]["lon"]

    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric&lang=pt_br"

    dados = requests.get(url).json()

    temp = dados["main"]["temp"]
    clima = dados["weather"][0]["description"]

    await update.message.reply_text(
        f"🌡 Temperatura: {temp}°C\n🌥 Condição: {clima}"
    )

# CHUVA PRÓXIMAS HORAS
async def chuva_horas(update: Update, context: ContextTypes.DEFAULT_TYPE):

    chat_id = update.message.chat_id

    if chat_id not in usuarios:
        await update.message.reply_text("📍 Envie sua localização primeiro.")
        return

    lat = usuarios[chat_id]["lat"]
    lon = usuarios[chat_id]["lon"]

    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"

    dados = requests.get(url).json()

    chuva = dados["list"][0]["pop"] * 100

    await update.message.reply_text(
        f"🌧 Chance de chuva nas próximas horas: {chuva:.0f}%"
    )

# PREVISÃO SEMANA
async def previsao_semana(update: Update, context: ContextTypes.DEFAULT_TYPE):

    chat_id = update.message.chat_id

    if chat_id not in usuarios:
        await update.message.reply_text("📍 Envie sua localização primeiro.")
        return

    lat = usuarios[chat_id]["lat"]
    lon = usuarios[chat_id]["lon"]

    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric&lang=pt_br"

    dados = requests.get(url).json()

    texto = "📅 Previsão próximos dias\n\n"

    for i in range(0, 40, 8):

        dia = dados["list"][i]

        data = datetime.fromtimestamp(dia["dt"]).strftime("%d/%m")

        temp = dia["main"]["temp"]

        clima = dia["weather"][0]["description"]

        texto += f"{data} → {temp:.1f}°C | {clima}\n"

    await update.message.reply_text(texto)

# RADAR
async def radar(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "🛰 Radar meteorológico:\nhttps://www.rainviewer.com/map.html"
    )

# ALERTA AUTOMÁTICO
async def alerta_chuva(context: ContextTypes.DEFAULT_TYPE):

    for chat_id, dados_usuario in usuarios.items():

        lat = dados_usuario["lat"]
        lon = dados_usuario["lon"]

        url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"

        dados = requests.get(url).json()

        chuva = dados["list"][0]["pop"] * 100

        if chuva >= 60:

            await context.bot.send_message(
                chat_id,
                f"🌧 ALERTA DE CHUVA\nChance de chuva: {chuva:.0f}% nas próximas horas."
            )

# BOT
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))

app.add_handler(MessageHandler(filters.LOCATION, receber_localizacao))

app.add_handler(MessageHandler(filters.Regex("Clima agora"), clima))
app.add_handler(MessageHandler(filters.Regex("Chuva próximas horas"), chuva_horas))
app.add_handler(MessageHandler(filters.Regex("Previsão semana"), previsao_semana))
app.add_handler(MessageHandler(filters.Regex("Radar de chuva"), radar))

# verificar chuva a cada 15 minutos
app.job_queue.run_repeating(alerta_chuva, interval=900, first=10)

print("BOT CLIMA ONLINE")

app.run_polling()