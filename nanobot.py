import requests
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = "8525579637:AAEsjWlG7WVIPdXDqWG1z4asKEV5S6oktTY"
API_KEY = "c76fbec0e18645652a17c73903e13e49"

LAT = -8.5844
LON = -39.8127


def clima():
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={LAT}&lon={LON}&appid={API_KEY}&units=metric&lang=pt_br"
    r = requests.get(url).json()

    temp = r["main"]["temp"]
    umidade = r["main"]["humidity"]
    vento = r["wind"]["speed"]
    condicao = r["weather"][0]["description"]

    return f"""
☁️ Clima atual

🌡️ Temperatura: {temp}°C
💧 Umidade: {umidade}%
💨 Vento: {vento} m/s
🌥️ Condição: {condicao}
"""


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    teclado = ReplyKeyboardMarkup(
        [["clima"]],
        resize_keyboard=True
    )

    await update.message.reply_text(
        "🌤️ BOT DO CLIMA\n\nClique no botão:",
        reply_markup=teclado
    )


async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):

    texto = update.message.text.lower()

    if texto == "clima":
        await update.message.reply_text(clima())


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT, responder))

print("BOT ONLINE")

app.run_polling()