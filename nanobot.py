from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import requests

TOKEN = "8525579637:AAEsjWlG7WVIPdXDqWG1z4asKEV5S6oktTY"

LAT = -8.5844
LON = -39.8127
API = "c76fbec0e18645652a17c73903e13e49"


# ===== CLIMA ATUAL =====
async def clima(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={LAT}&lon={LON}&appid={API}&units=metric&lang=pt_br"
    r = requests.get(url).json()

    temp = r["main"]["temp"]
    sens = r["main"]["feels_like"]
    hum = r["main"]["humidity"]
    vento = r["wind"]["speed"]
    desc = r["weather"][0]["description"]

    texto = f"""
☁️ Clima atual

🌡️ Temperatura: {temp}°C
🥵 Sensação térmica: {sens}°C
💧 Umidade: {hum}%
💨 Vento: {vento} m/s
🌥️ Condição: {desc}
"""

    await update.message.reply_text(texto)


# ===== START =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    teclado = [
        ["🌡️ Clima agora"],
        ["📅 Previsão semana"],
        ["🌧️ Chance de chuva"]
    ]

    reply_markup = ReplyKeyboardMarkup(teclado, resize_keyboard=True)

    await update.message.reply_text(
        "☀️ BOT DO CLIMA\n\nEscolha uma opção:",
        reply_markup=reply_markup
    )


# ===== RESPOSTA DOS BOTÕES =====
async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):

    texto = update.message.text

    if texto == "🌡️ Clima agora":
        await clima(update, context)

    elif texto == "📅 Previsão semana":
        await update.message.reply_text("📅 Função em construção")

    elif texto == "🌧️ Chance de chuva":
        await update.message.reply_text("🌧️ Função em construção")


# ===== BOT =====
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))

app.run_polling()