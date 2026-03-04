import requests
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN="8525579637:AAEsjWlG7WVIPdXDqWG1z4asKEV5S6oktTY"
API_KEY="c76fbec0e18645652a17c73903e13e49"

usuarios={}

# ---------------- START ----------------

async def start(update:Update,context:ContextTypes.DEFAULT_TYPE):

    botao=KeyboardButton("📍 Enviar localização",request_location=True)

    teclado=ReplyKeyboardMarkup([[botao]],resize_keyboard=True)

    await update.message.reply_text(
        "🌦️ BOT CLIMÁTICO COMPLETO\n\n"
        "Envie sua localização para ver a previsão completa 👇",
        reply_markup=teclado
    )

# ---------------- LOCALIZAÇÃO ----------------

async def local(update:Update,context:ContextTypes.DEFAULT_TYPE):

    lat=update.message.location.latitude
    lon=update.message.location.longitude
    chat_id=update.message.chat_id

    usuarios[chat_id]=(lat,lon)

# clima atual

    clima=requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric&lang=pt_br"
    ).json()

# previsão

    prev=requests.get(
        f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric&lang=pt_br"
    ).json()

    cidade=clima.get("name","Sua região")

    cond=clima["weather"][0]["main"].lower()

    emoji="☀️"

    if "cloud" in cond:
        emoji="☁️"

    if "rain" in cond:
        emoji="🌧️"

    if "storm" in cond:
        emoji="⛈️"

    chuva=int(prev["list"][0]["pop"]*100)

# ---------------- ZONA ----------------

    zona="🌾 Zona Rural"

    geo=requests.get(
        f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json",
        headers={"User-Agent":"bot"}
    ).json()

    if "address" in geo:

        addr=geo["address"]

        if "city" in addr or "town" in addr:
            zona="🏙️ Zona Urbana"

        if "village" in addr or "farm" in addr or "hamlet" in addr:
            zona="🌾 Zona Rural"

# ---------------- CLIMA ----------------

    texto=(
        f"{emoji} Clima em {cidade}\n\n"
        f"🌡️ Temperatura: {clima['main']['temp']}°C\n"
        f"🥵 Sensação térmica: {clima['main']['feels_like']}°C\n"
        f"💧 Umidade: {clima['main']['humidity']}%\n"
        f"💨 Vento: {clima['wind']['speed']} m/s\n"
        f"🌥️ Condição: {clima['weather'][0]['description']}\n"
        f"🌧️ Chance de chuva: {chuva}%\n\n"
        f"📍 Zona: {zona}\n"
        f"📍 Coordenadas: {round(lat,4)}, {round(lon,4)}"
    )

    await update.message.reply_text(texto)

# ---------------- PREVISÃO HORAS ----------------

    horas="\n⏰ Próximas horas\n\n"

    for bloco in prev["list"][:6]:

        hora=bloco["dt_txt"].split(" ")[1][:5]

        chance=int(bloco["pop"]*100)

        mm=0

        if "rain" in bloco and "3h" in bloco["rain"]:
            mm=bloco["rain"]["3h"]

        horas+=f"{hora} → {chance}% | {mm}mm\n"

    await update.message.reply_text(horas)

# ---------------- PREVISÃO DIAS ----------------

    dias="\n📅 Próximos dias\n\n"

    usados=set()

    for bloco in prev["list"]:

        data=bloco["dt_txt"].split(" ")[0]

        if data not in usados:

            usados.add(data)

            temp=bloco["main"]["temp"]

            desc=bloco["weather"][0]["description"]

            dias+=f"{data} → {temp}°C | {desc}\n"

        if len(usados)==5:
            break

    await update.message.reply_text(dias)

# ---------------- RADAR ----------------

    radar=f"https://www.rainviewer.com/weather-radar-map-live.html?lat={lat}&lon={lon}&zoom=7"

    await update.message.reply_text(
        f"🛰️ Radar de chuva da sua região:\n{radar}"
    )

# ---------------- ALERTA ----------------

async def alerta(context:ContextTypes.DEFAULT_TYPE):

    for chat_id,(lat,lon) in usuarios.items():

        prev=requests.get(
            f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
        ).json()

        chance=int(prev["list"][0]["pop"]*100)

        if chance>=80:

            await context.bot.send_message(
                chat_id,
                f"⚠️ ALERTA DE CHUVA FORTE\n\nChance de chuva: {chance}% 🌧️"
            )

# ---------------- BOT ----------------

app=ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start",start))
app.add_handler(MessageHandler(filters.LOCATION,local))

app.job_queue.run_repeating(alerta,interval=600,first=20)

print("🌦️ Bot climático completo rodando...")

app.run_polling()