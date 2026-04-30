import telebot
from telebot import types
import google.generativeai as genai
import os
from flask import Flask
from threading import Thread

# --- Flask Server (Render ላይ ቦቱ እንዳይዘጋ ለመርዳት) ---
server = Flask(__name__)

@server.route("/")
def home():
    return "AA Smart Bot is Online and Ready!"

# --- Configuration ---
TOKEN = '8513514659:AAFEWJ647fRyfNhasIvT-IyJDJR5gD5an-8'
# አዲሱን API Key እዚህ ጋር አስገብቼልሃለሁ
API_KEY = 'AIzaSyAbcfnu7CXmfXvjxshiYrxQJJXLIQ4ZxhU'
ADMIN_ID = '7266453062'

# --- Gemini AI Setup ---
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
    welcome_text = (
        "✨ **እንኳን ወደ AA COMPANY Smart Bot በደህና መጡ!** ✨\n\n"
        "እኔ በ Gemini AI የታገዝኩ ረዳት ነኝ። በ AI ጥያቄ ለመጠየቅ '🤖 በ AI ጠይቅ' የሚለውን ይጫኑ።"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=get_main_menu(), parse_mode="Markdown")

# --- Button Handlers ---
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    chat_id = call.message.chat.id
    
    if call.data == "ai_mode":
        msg = bot.send_message(chat_id, "🤖 **የ AI ሞድ በርቷል!**\n\nአሁን ማንኛውንም ጥያቄ መጻፍ ይችላሉ። (ለመውጣት 'ወጣ' ወይም 'exit' ይበሉ)፦")
        bot.register_next_step_handler(msg, handle_ai_chat)
        
    elif call.data == "about_aa":
        about_text = (
            "🏢 **ስለ AA COMPANY**\n\n"
            "AA COMPANY የቴክኖሎጂ ፈጠራዎችን፣ የዲጂታል ክህሎቶችን እና "
            "ዘመናዊ የትምህርት መርጃዎችን ለተጠቃሚዎች የሚያቀርብ ተቋም ነው።"
        )
        bot.send_message(chat_id, about_text, parse_mode="Markdown")
        
    elif call.data == "formulas":
        formula_text = (
            "📐 **ጠቃሚ ፎርሙላዎች**\n\n"
            "• **Physics:** $F = m \cdot a$\n"
            "• **Math:** $A = \pi r^2$\n"
            "• **Einstein:** $E = mc^2$"
        )
        bot.send_message(chat_id, formula_text, parse_mode="Markdown")

    elif call.data == "passive_income":
        income_text = "💰 **ተገቢ ገቢ (Passive Income)**\n\nበመስመር ላይ ገቢ ማግኘት የሚቻልባቸውን መንገዶች እና የተለያዩ ዲጂታል ክህሎቶችን እዚህ እናሳውቃለን።"
        bot.send_message(chat_id, income_text, parse_mode="Markdown")

    elif call.data == "ask_question":
        msg = bot.send_message(chat_id, "❓ ጥያቄዎን እዚህ ይጻፉልኝ። በቀጥታ ለአስተዳዳሪው ይደርሳል።")
        bot.register_next_step_handler(msg, forward_to_admin)

    bot.answer_callback_query(call.id)

# --- AI Chat Logic ---
def handle_ai_chat(message):
    if message.text.lower() in ['exit', 'ወጣ', '/start', 'back']:
        bot.send_message(message.chat.id, "ከ AI ሞድ ወጥተዋል።", reply_markup=get_main_menu())
        return

    bot.send_chat_action(message.chat.id, 'typing')
    try:
        response = model.generate_content(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, "⚠️ AIው መልስ ለመስጠት ተቸግሯል። እባክዎ ትንሽ ቆይተው ይሞክሩ።")
    
    msg = bot.send_message(message.chat.id, "ሌላ ጥያቄ ካለዎት ይቀጥሉ (ወይም 'ወጣ' ይበሉ)፦")
    bot.register_next_step_handler(msg, handle_ai_chat)

# --- Admin Forwarding ---
def forward_to_admin(message):
    user_info = f"👤 {message.from_user.first_name}\n🆔 ID: {message.from_user.id}"
    bot.send_message(ADMIN_ID, f"📩 **አዲስ ጥያቄ**፦\n\n{message.text}\n\n{user_info}")
    bot.send_message(message.chat.id, "✅ መልእክትዎ ደርሷል!", reply_markup=get_main_menu())

# --- Admin Reply Logic ---
@bot.message_handler(func=lambda message: message.reply_to_message is not None and str(message.chat.id) == ADMIN_ID)
def reply_to_user(message):
    try:
        target_id = message.reply_to_message.text.split("ID: ")[1].strip()
        bot.send_message(target_id, f"📩 **ከ AA COMPANY የተላከ መልስ**፦\n\n{message.text}")
        bot.reply_to(message, "✅ መልስዎ ተልኳል።")
    except:
        bot.reply_to(message, "❌ ስህተት፡ መልሱን መላክ አልተቻለም።")

# --- ማስነሻ ---
if __name__ == "__main__":
    Thread(target=lambda: bot.infinity_polling()).start()
    port = int(os.environ.get("PORT", 5000))
    server.run(host="0.0.0.0", port=port)
