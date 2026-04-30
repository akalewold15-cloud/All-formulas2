import telebot
from telebot import types
import google.generativeai as genai
import os
from flask import Flask
from threading import Thread

# --- Flask Server (For Render Port) ---
server = Flask(__name__)

@server.route("/")
def home():
    return "AA Smart Bot is Online!"

# --- configuration ---
TOKEN = '8513514659:AAFEWJ647fRyfNhasIvT-IyJDJR5gD5an-8'
API_KEY = 'AIzaSyBRFThyLfz94J__xxzoWJ6qJcaKYF9pCtc'
ADMIN_ID = '7266453062'

# --- Gemini AI Setup (አሁን ተስተካክሏል) ---
genai.configure(api_key=API_KEY)
# እዚህ ጋር 'gemini-1.5-flash' የሚለው የግድ ያስፈልጋል
model = genai.GenerativeModel('gemini-1.5-flash') 

bot = telebot.TeleBot(TOKEN)

# --- የሜኑ አዝራሮች ---
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
    bot.send_message(message.chat.id, "ሰላም! የ AA COMPANY ረዳት ቦት ነው። ምን ላግዝዎት?", 
                     reply_markup=get_main_menu())

# --- አዝራሮች ሲነኩ ---
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "ai_mode":
        msg = bot.send_message(call.message.chat.id, "🤖 AI ሞድ በርቷል። ጥያቄዎን ይጻፉ (ለመውጣት 'exit' ይበሉ)፦")
        bot.register_next_step_handler(msg, handle_ai_chat)
    elif call.data == "about_aa":
        # እዚህ ጋር ስለ ኩባንያው የምትጽፈው ባዶ ስለነበር ነው የማይሰራው
        about_text = "🏢 **ስለ AA COMPANY**፦\n\n(እዚህ ጋር የኩባንያህን መረጃ ማስገባት ትችላለህ። ለምሳሌ፦ አድራሻ፣ ስራዎች...)"
        bot.send_message(call.message.chat.id, about_text, parse_mode="Markdown")
    elif call.data == "ask_question":
        msg = bot.send_message(call.message.chat.id, "❓ ጥያቄዎን ይጻፉ፣ ለአስተዳዳሪው ይደርሳል።")
        bot.register_next_step_handler(msg, forward_to_admin)
    elif call.data == "formulas":
        bot.send_message(call.message.chat.id, "📐 **ፎርሙላዎች**፦\n\n• $F = ma$\n• $E = mc^2$", parse_mode="Markdown")
    elif call.data == "passive_income":
        bot.send_message(call.message.chat.id, "💰 **ተገቢ ገቢ**፦\n\n(እዚህ ጋር መረጃህን ጨምር)")
    
    bot.answer_callback_query(call.id)

# --- AI Chat ---
def handle_ai_chat(message):
    if message.text.lower() in ['exit', 'ወጣ', '/start']:
        bot.send_message(message.chat.id, "ከ AI ሞድ ወጥተዋል።", reply_markup=get_main_menu())
        return
    
    bot.send_chat_action(message.chat.id, 'typing')
    try:
        # AI-ው መልስ እንዲሰጥ ማዘዝ
        response = model.generate_content(message.text)
        bot.reply_to(message, response.text)
    except:
        bot.reply_to(message, "⚠️ AIው መልስ ለመስጠት ተቸግሯል። API Key-ህን ወይም ኢንተርኔትህን አረጋግጥ።")
    
    # ተከታታይ ጥያቄ እንዲቀበል
    msg = bot.send_message(message.chat.id, "ሌላ ጥያቄ? (ወይም 'exit' ይበሉ)")
    bot.register_next_step_handler(msg, handle_ai_chat)

# --- Admin Forwarding ---
def forward_to_admin(message):
    user_info = f"🆔 ID: {message.from_user.id}"
    bot.send_message(ADMIN_ID, f"📩 **ጥያቄ**፦\n{message.text}\n\n{user_info}")
    bot.send_message(message.chat.id, "✅ መልእክትዎ ደርሷል!", reply_markup=get_main_menu())

# --- Admin Reply ---
@bot.message_handler(func=lambda message: message.reply_to_message is not None and str(message.chat.id) == ADMIN_ID)
def reply_to_user(message):
    try:
        target_id = message.reply_to_message.text.split("ID: ")[1].strip()
        bot.send_message(target_id, f"📩 **ከ AA COMPANY**፦\n\n{message.text}")
        bot.reply_to(message, "✅ ተልኳል።")
    except:
        bot.reply_to(message, "❌ መላክ አልተቻለም።")

# --- ማስነሻ ---
if __name__ == "__main__":
    Thread(target=lambda: bot.infinity_polling()).start()
    port = int(os.environ.get("PORT", 5000))
    server.run(host="0.0.0.0", port=port)
