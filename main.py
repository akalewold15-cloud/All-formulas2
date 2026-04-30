import telebot
from telebot import types
from google import genai  # አዲሱ አጻጻፍ እንዲህ ነው
import os
from flask import Flask
from threading import Thread

# --- Flask Server ---
server = Flask(__name__)
@server.route("/")
def home(): return "Bot is Online!"

# --- Config ---
TOKEN = '8513514659:AAFEWJ647fRyfNhasIvT-IyJDJR5gD5an-8'
API_KEY = 'AIzaSyAbcfnu7CXmfXvjxshiYrxQJJXLIQ4ZxhU'

# --- Gemini API Client Setup (አዲሱ መንገድ) ---
client = genai.Client(AIzaSyAbcfnu7CXmfXvjxshiYrxQJJXLIQ4ZxhU)
bot = telebot.TeleBot(8513514659:AAFEWJ647fRyfNhasIvT-IyJDJR5gD5an-8)

# --- AI Chat Logic ---
def handle_ai_chat(message):
    if message.text.lower() in ['exit', 'ወጣ']:
        bot.send_message(message.chat.id, "ወደ ዋናው ሜኑ ተመልሰዋል።")
        return

    bot.send_chat_action(message.chat.id, 'typing')
    try:
        # አዲሱ የጥያቄ አጻጻፍ ዘዴ (በምስሉ ላይ እንዳለው)
        response = client.models.generate_content(
            model="gemini-1.5-flash", 
            contents=message.text
        )
        bot.reply_to(message, response.text)
    except Exception as e:
        print(f"Error: {e}")
        bot.reply_to(message, "⚠️ ችግር ተፈጥሯል። በኋላ ይሞክሩ።")
    
    msg = bot.send_message(message.chat.id, "ሌላ ጥያቄ ካለዎት ይቀጥሉ (ወይም 'ወጣ' ይበሉ)፦")
    bot.register_next_step_handler(msg, handle_ai_chat)

# --- Start & Menu ---
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🤖 በ AI ጠይቅ", callback_data="ai_mode"))
    bot.send_message(message.chat.id, "ሰላም! የ AA COMPANY ቦት ነው።", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "ai_mode")
def ai_start(call):
    msg = bot.send_message(call.message.chat.id, "🤖 ጥያቄዎን ይጻፉልኝ፦")
    bot.register_next_step_handler(msg, handle_ai_chat)

# --- Run ---
if __name__ == "__main__":
    Thread(target=lambda: bot.infinity_polling(skip_pending=True)).start()
    port = int(os.environ.get("PORT", 5000))
    server.run(host="0.0.0.0", port=port)
