import requests
from datetime import datetime, timedelta
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = "8525579637:AAEsjWlG7WVIPdXDqWG1z4asKEV5S6oktTY"
API_KEY = "c76fbec0e18645652a17c73903e13e49"

# MENU
menu = [
    ["📍 Enviar localização"],
    ["🌡 Clima agora"],
    ["🌧 Chuva próximas horas"],
    ["📅 Previsão semana"],
    ["🛰 Radar de chuva"]
]

markup = ReplyKeyboardMarkup(menu, resize_keyboard=True)

# COMANDO START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌤 BOT DO CLIMA\nEnvie sua localização ou escolha uma opção:",
        reply_markup=markup
    )

# CLIMA AGORA
async def clima(update: Update, context: ContextTypes.DEFAULT_TYPE):

    cidade = "Santa Maria da Boa Vista,BR"

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

    resposta = f"""
☀️ Clima em Santa Maria da Boa Vista

🌡 Temperatura: {temp:.2f}°C
🥵 Sensação térmica: {sensacao:.2f}°C
💧 Umidade: {umidade}%
💨 Vento: {vento} m/s
🌥 Condição: {clima}

🌅 Nascer do sol: {nascer_sol.strftime("%H:%M")}
🌇 Pôr do sol: {por_sol.strftime("%H:%M")}
"""

    await update.message.reply_text(resposta)

# CHUVA PRÓXIMAS HORAS
async def chuva_horas(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "🌧 Analisando previsão das próximas horas..."
    )

# PREVISÃO SEMANA
async def previsao_semana(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "📅 Buscando previsão da semana..."
    )

# RADAR DE CHUVA
async def radar(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "🛰 Radar meteorológico em breve..."
    )

# INICIAR BOT
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))

app.add_handler(MessageHandler(filters.Regex("Clima agora"), clima))
app.add_handler(MessageHandler(filters.Regex("Chuva próximas horas"), chuva_horas))
app.add_handler(MessageHandler(filters.Regex("Previsão semana"), previsao_semana))
app.add_handler(MessageHandler(filters.Regex("Radar de chuva"), radar))

print("BOT CLIMA ONLINE")

app.run_polling()