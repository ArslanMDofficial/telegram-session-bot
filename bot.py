import telebot
from flask import Flask
import threading

# 🔒 Apna Telegram Bot Token yahan daalo
BOT_TOKEN = '7729339808:AAFidl9o1vk3jmZui4J3toChJL0RJMImQzs'
bot = telebot.TeleBot(BOT_TOKEN)

# ✅ Welcome Message
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "👋 Welcome to *Sarkar-MD Session Generator Bot!*\n\n"
        "📌 *Developer:* ArslanMD Official\n"
        "📺 *YouTube:* [Click Here](https://youtube.com/@arslanmdofficial?si=QgcrLCaRz-Pqya-n)\n"
        "📱 *WhatsApp Channel:* [Join Now](https://whatsapp.com/channel/0029VarfjW04tRrmwfb8x306)\n\n"
        "🔐 Send your phone number with country code (without +) to get started."
    )
    bot.send_message(message.chat.id, welcome_text, parse_mode='Markdown')

# ✅ Yeh example handler hai — apna logic yahan daalo
@bot.message_handler(func=lambda m: True)
def echo_all(message):
    phone = message.text.strip()
    if phone.isdigit():
        bot.reply_to(message, f"📲 Pairing code banaya ja raha hai for: `{phone}`", parse_mode="Markdown")
        # Yahan apna Koyeb ya backend logic daal do jo session ID banata hai
        session_id = "Sarkarmd$eyJzZXNzaW9uIjogIkV4YW1wbGUifQ=="  # Sample ID
        bot.send_message(message.chat.id, f"✅ Session ID:\n`{session_id}`", parse_mode="Markdown")
    else:
        bot.reply_to(message, "❌ Invalid number. Please send digits only (with country code, no +).")

# ✅ Flask App for Render health check
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running fine!"

def run_flask():
    app.run(host="0.0.0.0", port=8000)

# ✅ Start Flask in background
flask_thread = threading.Thread(target=run_flask)
flask_thread.start()

# ✅ Start Telegram polling
print("✅ Bot is running with polling...")
bot.infinity_polling()
