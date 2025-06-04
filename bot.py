import telebot  
from flask import Flask  
import threading  
import requests  
  
BOT_TOKEN = '7729339808:AAFidl9o1vk3jmZui4J3toChJL0RJMImQzs'  
bot = telebot.TeleBot(BOT_TOKEN)  
  
# ✅ Welcome  
@bot.message_handler(commands=['start'])  
def send_welcome(message):  
    welcome_text = (  
        "👋 Welcome to *Sarkar-MD Session Generator Bot!*\n\n"  
        "📌 *Developer:* ArslanMD Official\n"  
        "📺 *YouTube:* [Click Here](https://youtube.com/@arslanmdofficial?si=QgcrLCaRz-Pqya-n)\n"  
        "📱 *WhatsApp Channel:* [Join Now](https://whatsapp.com/channel/0029VarfjW04tRrmwfb8x306)\n\n"  
        "🔐 Apna number (bina '+') bhejein pairing code hasil karne ke liye."  
    )  
    bot.send_message(message.chat.id, welcome_text, parse_mode='Markdown')  
  
# ✅ Number Handler  
@bot.message_handler(func=lambda m: True)  
def generate_session(message):  
    phone = message.text.strip()  
    if phone.isdigit():  
        bot.send_message(message.chat.id, f"⏳ Pairing code banaya ja raha hai for `{phone}`...", parse_mode="Markdown")  
        try:  
            response = requests.get(f"https://sarkar-md-session.koyeb.app/number?phone={phone}")  
            if response.status_code == 200:  
                result = response.json()  
                if 'session' in result:  
                    session_id = result['session']  
                    bot.send_message(message.chat.id, f"✅ *Session ID mil gaya:*\n`{session_id}`", parse_mode="Markdown")  
                elif 'code' in result:  
                    code = result['code']  
                    bot.send_message(message.chat.id, f"🔑 *Pairing Code:* `{code}`\n\n📲 Please open WhatsApp > Linked Devices > Link with code.", parse_mode="Markdown")  
                else:  
                    bot.send_message(message.chat.id, "⚠️ Koi valid response nahi mila.")  
            else:  
                bot.send_message(message.chat.id, "❌ Server error. Thodi dair baad koshish karein.")  
        except Exception as e:  
            bot.send_message(message.chat.id, f"❌ Error: {str(e)}")  
    else:  
        bot.send_message(message.chat.id, "❌ Ghalat format. Sirf number bhejein (country code ke saath, bina '+').")  
  
# ✅ Flask for health check  
app = Flask(__name__)  
  
@app.route('/')  
def home():  
    return "Bot is running fine!"  
  
def run_flask():  
    app.run(host="0.0.0.0", port=8000)  
  
# ✅ Run Flask  
flask_thread = threading.Thread(target=run_flask)  
flask_thread.start()  
  
# ✅ Polling  
print("✅ Bot is running with polling...")  
bot.infinity_polling()
