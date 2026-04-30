import telebot
from telebot import types
import google.generativeai as genai
import os
from flask import Flask

# --- Render Web Service እንዲሰራ የሚረዳ (Port fix) ---
server = Flask(__name__)

@server.route("/")
def home():
    return "AA Smart Bot is Running!"

# --- ኮንፊገሬሽን ---
TOKEN = '8513514659:AAFEWJ647fRyfNhasIvT-IyJDJR5gD5an-8'
API_KEY = 'AIzaSyBRFThyLfz94J__xxzoWJ6qJcaKYF9pCtc'
ADMIN_ID = '7266453062'

# Gemini AI Setup
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

bot = telebot.TeleBot(TOKEN)

# --- የዋና ሜኑ አዝራሮች ---
def get_main_menu():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🤖 በ AI ጠይቅ", callback_data="ai_mode"),
        types.InlineKeyboardButton("🏢 ስለ AA COMPANY", callback_data="about_aa"),
        types.InlineKeyboardButton("📐 ፎርሙላዎች", callback_data="formulas"),
        types.InlineKeyboardButton("💰 ተገቢ ገቢ (Income)", callback_data="passive_income"),
        types.InlineKeyboardButton("❓ ጥያቄ ለመጠየቅ", callback_data="ask_question"),
        types.InlineKeyboardButton("📢 Join Channel", url="https://t.me/smart_kihilot")
    )
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "✨ *AA COMPANY Smart Bot* ✨\nአሁን ለ Web Service ተስተካክሏል። ምን ልርዳዎት?", 
                     reply_markup=get_main_menu(), parse_mode="Markdown")

# --- Button Handlers ---
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "ai_mode":
        msg = bot.send_message(call.message.chat.id, "🤖 *AI ሞድ በርቷል!* ጥያቄዎን ይጻፉ (ለመውጣት 'exit' ይበሉ)፦")
        bot.register_next_step_handler(msg, handle_ai_chat)
    elif call.data == "ask_question":
        msg = bot.send_message(call.message.chat.id, "❓ ጥያቄዎን ይጻፉ፣ ለአስተዳዳሪው ይደርሳል።")
        bot.register_next_step_handler(msg, forward_to_admin)
    elif call.data == "formulas":
        bot.send_message(call.message.chat.id, "📐 *ፎርሙላዎች*፦\n$F = m \cdot a$\n$A = \pi r^2$", parse_mode="Markdown")
    # ... ሌሎቹን እንደፈለግክ መጨመር ትችላለህ
    bot.answer_callback_query(call.id)

# --- AI Logic ---
def handle_ai_chat(message):
    if message.text.lower() in ['exit', 'ወጣ', '/start']:
        bot.send_message(message.chat.id, "ከ AI ሞድ ወጥተዋል።", reply_markup=get_main_menu())
        return
    bot.send_chat_action(message.chat.id, 'typing')
    try:
        response = model.generate_content(message.text)
        bot.reply_to(message, response.text)
    except:
        bot.reply_to(message, "⚠️ AIው ለጊዜው አልሰራም።")
    msg = bot.send_message(message.chat.id, "ሌላ ጥያቄ ካለዎት ይቀጥሉ፦")
    bot.register_next_step_handler(msg, handle_ai_chat)

# --- Admin Logic ---
def forward_to_admin(message):
    user_info = f"🆔 ID: {message.from_user.id}"
    bot.send_message(ADMIN_ID, f"📩 *ጥያቄ*፦\n{message.text}\n\n{user_info}", parse_mode="Markdown")
    bot.send_message(message.chat.id, "✅ ተልኳል!", reply_markup=get_main_menu())

@bot.message_handler(func=lambda message: message.reply_to_message is not None and str(message.chat.id) == ADMIN_ID)
def reply_to_user(message):
    try:
        target_id = message.reply_to_message.text.split("ID: ")[1].strip()
        bot.send_message(target_id, f"📩 *ከ AA COMPANY*፦\n\n{message.text}")
        bot.reply_to(message, "✅ ተልኳል።")
    except:
        bot.reply_to(message, "❌ መላክ አልተቻለም።")

# --- ቦቱን የማስነሻ ዘዴ ለ Web Service ---
if __name__ == "__main__":
    # Render Port fix
    from threading import Thread
    def run_bot():
        bot.infinity_polling()

    # ቦቱን በሌላ Thread ያስነሳል
    Thread(target=run_bot).start()
    
    # Flask (Web Server) Render እንዲያየው ያስነሳል
    port = int(os.environ.get("PORT", 5000))
    server.run(host="0.0.0.0", port=port)
