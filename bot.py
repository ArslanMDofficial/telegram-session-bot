import requests
from telegram import Update, ForceReply
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Replace this with your actual Telegram Bot Token
BOT_TOKEN = "7729339808:AAH1wUH6pmH7qUoVZvZnbQj44-uPUC0S2sI"

# Store user states (number entered or not)
user_states = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Assalamualaikum! WhatsApp session ID hasil karne ke liye apna number bhejein (without +).\n\nExample: 923001234567"
    )
    user_states[update.effective_chat.id] = "waiting_for_number"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_input = update.message.text.strip()

    if user_states.get(chat_id) == "waiting_for_number":
        if not user_input.isdigit():
            await update.message.reply_text("❌ Sirf numbers bhejein. Format: 923001234567")
            return
        
        await update.message.reply_text("🔄 Pairing code hasil kiya ja raha hai...")

        try:
            response = requests.get(f"https://sarkar-md-session-generator.koyeb.app/code?number={user_input}")
            if response.status_code == 200:
                code = response.text
                await update.message.reply_text(
                    f"✅ Pairing code: `{code}`\n\n🔗 WhatsApp open karen → Linked Devices → Add Device → Pair with code\n\n⌛ 30 seconds ke baad /session likhein apna session hasil karne ke liye.",
                    parse_mode='Markdown'
                )
                user_states[chat_id] = user_input  # Save number for session later
            else:
                await update.message.reply_text("❌ Code lene mein error aaya. Dobara koshish karein.")
        except Exception as e:
            await update.message.reply_text(f"⚠️ Error: {e}")
    
    else:
        await update.message.reply_text("❗ Pehle /start likhein aur apna number bhejein.")

async def get_session(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    number = user_states.get(chat_id)

    if not number or not number.startswith("92"):
        await update.message.reply_text("❗ Pehle apna number bhejein. /start likhein dobara shuru karne ke liye.")
        return

    await update.message.reply_text("🔍 Session ID hasil ki ja rahi hai...")

    try:
        response = requests.get(f"https://sarkar-md-session-generator.koyeb.app/getSession?number={number}")
        if response.status_code == 200 and response.text.startswith("Sarkarmd$"):
            await update.message.reply_text(f"✅ Session ID mil gaya:\n\n`{response.text}`", parse_mode='Markdown')
            user_states.pop(chat_id)
        else:
            await update.message.reply_text("❌ Abhi tak WhatsApp pair nahi hua. Thodi dair baad /session likhein.")
    except Exception as e:
        await update.message.reply_text(f"⚠️ Error: {e}")

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("session", get_session))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Bot is running...")
    app.run_polling()
