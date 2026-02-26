!pip install python-telegram-bot requests nest_asyncio -q

import requests
import asyncio
import nest_asyncio
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes

nest_asyncio.apply()  # Colab uchun muhim!

API_KEY_PLATE = "6a12ba74a191b6121098e682ae1ff776433669eb"
TELEGRAM_TOKEN = "8710071083:AAHcmIT7Q2JeqljFG6Nj871X1W-qgEGKcEE"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Salom! 👋\nMashina rasmini yuboring, davlat raqamini aniqlayman."
    )

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Rasm qabul qilindi, tekshirilmoqda...")
    
    photo = update.message.photo[-1]
    file = await context.bot.get_file(photo.file_id)
    file_path = "temp_car.jpg"
    await file.download_to_drive(file_path)
    
    with open(file_path, "rb") as img:
        response = requests.post(
            "https://api.platerecognizer.com/v1/plate-reader/",
            headers={"Authorization": f"Token {API_KEY_PLATE}"},
            files={"upload": img},
            data={"regions": ["uz"]}
        )
    
    result = response.json()
    
    if result["results"]:
        plate = result["results"][0]["plate"].upper()
        confidence = result["results"][0]["score"]
        await update.message.reply_text(
            f"🚗 Davlat raqami: <b>{plate}</b>\n"
            f"✅ Aniqlik: {confidence:.0%}",
            parse_mode="HTML"
        )
    else:
        await update.message.reply_text("❌ Raqam aniqlanmadi. Rasmni aniqroq yuboring.")

async def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    print("Bot ishga tushdi...")
    await app.run_polling()

asyncio.get_event_loop().run_until_complete(main())
