import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import requests

TOKEN = "YOUR_BOT_TOKEN_HERE"

logging.basicConfig(level=logging.INFO)

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome! Apna WhatsApp number dein (without +), jaise 923001234567:")

# Handle phone number
async def handle_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    number = update.message.text.strip()
    await update.message.reply_text(f"Number mila: {number}\nPairing code generate kiya ja raha hai...")

    # Pairing code API
    pairing_url = f"https://sarkar-md-session-generator.koyeb.app/code?number={number}"
    resp = requests.get(pairing_url)

    if resp.status_code == 200 and "code" in resp.json():
        code = resp.json()['code']
        await update.message.reply_text(f"Pairing code: `{code}`\n\nApne WhatsApp me ja kar *Linked Devices* me jayein aur 'Link a Device' pe click kar ke yeh code paste karein.\n\nJab WhatsApp link ho jaye, /getsession likhein.", parse_mode='Markdown')
        context.user_data["number"] = number
    else:
        await update.message.reply_text("Kuch ghalat ho gaya! Number sahi format me dein.")

# Get session ID
async def getsession(update: Update, context: ContextTypes.DEFAULT_TYPE):
    number = context.user_data.get("number")
    if not number:
        await update.message.reply_text("Pehle apna number dein!")
        return

    session_url = f"https://sarkar-md-session-generator.koyeb.app/session?number={number}"
    resp = requests.get(session_url)

    if resp.status_code == 200 and "session" in resp.json():
        session = resp.json()['session']
        await update.message.reply_text(f"✅ Aapka session ID:\n\n`{session}`\n\nIsay apne bot repo me add kar ke deploy karen.", parse_mode='Markdown')
    else:
        await update.message.reply_text("Session abhi tak generate nahi hua. Thori dair baad try karein.")

# Main function
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("getsession", getsession))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_number))
    app.run_polling()

if __name__ == "__main__":
    main()
