import telebot
from telebot import types
from google import genai  # google-genai መጫኑን አረጋግጥ
import os
from flask import Flask
from threading import Thread

# --- Flask Server (ለ Render ወይም ለሌላ ሆስቲንግ) ---
server = Flask(__name__)
@server.route("/")
def home(): 
    return "Bot is Online!"

# --- Config (ቁልፎቹን በጥቅስ ምልክት ውስጥ አድርጋቸው) ---
TOKEN = '8513514659:AAFEWJ647fRyfNhasIvT-IyJDJR5gD5an-8'
API_KEY = 'AIzaSyAbcfnu7CXmfXvjxshiYrxQJJXLIQ4ZxhU'

# --- Gemini API Client Setup ---
# እዚህ ጋር API_KEY የሚለውን ተለዋዋጭ እንጠቀማለን
client = genai.Client(api_key=API_KEY)
bot = telebot.TeleBot(TOKEN)

# --- AI Chat Logic ---
def handle_ai_chat(message):
    # ተጠቃሚው 'ወጣ' ካለ ከ AI ቻት ይወጣል
    if message.text.lower() in ['exit', 'ወጣ', '/stop']:
        bot.send_message(message.chat.id, "ወደ ዋናው ሜኑ ተመልሰዋል።")
        return

    bot.send_chat_action(message.chat.id, 'typing')
    try:
        # Gemini API ጥሪ
        response = client.models.generate_content(
            model="gemini-1.5-flash", 
            contents=message.text
        )
        bot.reply_to(message, response.text)
    except Exception as e:
        print(f"Error: {e}")
        bot.reply_to(message, "⚠️ ይቅርታ፣ ችግር አጋጥሞኛል። እባክዎ ትንሽ ቆይተው ይሞክሩ።")
    
    # ለሚቀጥለው ጥያቄ ተጠቃሚውን መጠበቅ (Loop)
    msg = bot.send_message(message.chat.id, "ሌላ ጥያቄ ካለዎት ይቀጥሉ (ወይም 'ወጣ' ይበሉ)፦")
    bot.register_next_step_handler(msg, handle_ai_chat)

# --- Start & Menu ---
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🤖 በ AI ጠይቅ", callback_data="ai_mode"))
    bot.send_message(message.chat.id, f"ሰላም {message.from_user.first_name}! የ AA COMPANY ቦት ነው። በምን ልርዳዎት?", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "ai_mode")
def ai_start(call):
    msg = bot.send_message(call.message.chat.id, "🤖 የፈለጉትን ጥያቄ ይጠይቁኝ (ለማቆም 'ወጣ' ይበሉ)፦")
    bot.register_next_step_handler(msg, handle_ai_chat)

# --- Run ---
def run_flask():
    port = int(os.environ.get("PORT", 5000))
    server.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    # Flaskን በሌላ Thread ማስጀመር
    Thread(target=run_flask).start()
    print("Bot is starting...")
    bot.infinity_polling(skip_pending=True)
