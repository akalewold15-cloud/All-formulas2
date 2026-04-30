import telebot
from telebot import types
import google.generativeai as genai

# መረጃዎች 2
TOKEN = '8513514659:AAFEWJ647fRyfNhasIvT-IyJDJR5gD5an-8'
API_KEY = 'AIzaSyBRFThyLfz94J__xxzoWJ6qJcaKYF9pCtc'
ADMIN_ID = '7266453062'

# Gemini Setup
try:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    print(f"AI Setup Error: {e}")

bot = telebot.TeleBot(TOKEN)

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
    bot.send_message(message.chat.id, "✨ *እንኳን ወደ AA COMPANY መጡ!* ✨\nምን ልርዳዎት?", 
                     reply_markup=get_main_menu(), parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "ai_mode":
        msg = bot.send_message(call.message.chat.id, "🤖 *የ AI ሞድ በርቷል!* አሁን ጥያቄዎን ይጻፉልኝ (ለምሳሌ፦ ስለ ፊዚክስ ጠይቁኝ)።")
        bot.register_next_step_handler(msg, handle_ai_chat)
    elif call.data == "ask_question":
        msg = bot.send_message(call.message.chat.id, "❓ ጥያቄዎን ይጻፉ፣ ለአስተዳዳሪው ይደርሳል።")
        bot.register_next_step_handler(msg, forward_to_admin)
    # ሌሎቹን አዝራሮች እዚህ ጋር መቀጠል ትችላለህ...
    bot.answer_callback_query(call.id)

# --- AI መልስ ሰጪ ክፍል ---
def handle_ai_chat(message):
    # ተጠቃሚው ሌላ አዝራር መጫን ከፈለገ ወይም ለመውጣት 'exit' ካለ
    if message.text.lower() in ['exit', 'ወጣ', '/start']:
        bot.send_message(message.chat.id, "ከ AI ሞድ ወጥተዋል።", reply_markup=get_main_menu())
        return

    bot.send_chat_action(message.chat.id, 'typing')
    try:
        # AI መልስ እንዲያመጣ ትእዛዝ
        response = model.generate_content(message.text)
        # መልሱ ባዶ እንዳይሆን ማረጋገጥ
        if response and response.text:
            bot.reply_to(message, response.text)
        else:
            bot.reply_to(message, "ይቅርታ፣ AI መልስ ሊሰጠኝ አልቻለም።")
    except Exception as e:
        print(f"AI Error: {e}")
        bot.reply_to(message, "⚠️ የ AI አገልግሎት ለጊዜው አልሰራም። እባክዎ ትንሽ ቆይተው ይሞክሩ።")
    
    # ተከታታይ ጥያቄ እንዲጠይቅ እንደገና ሬጅስተር እናደርጋለን
    msg = bot.send_message(message.chat.id, "ሌላ ጥያቄ ካለዎት ይቀጥሉ (ለመውጣት 'exit' ይበሉ)፦")
    bot.register_next_step_handler(msg, handle_ai_chat)

def forward_to_admin(message):
    user_info = f"👤 ከ: {message.from_user.first_name}\n🆔 ID: {message.from_user.id}"
    bot.send_message(ADMIN_ID, f"📩 *አዲስ ጥያቄ*፦\n\n{message.text}\n\n{user_info}", parse_mode="Markdown")
    bot.send_message(message.chat.id, "✅ መልእክትዎ ደርሷል!", reply_markup=get_main_menu())

if __name__ == "__main__":
    bot.infinity_polling()
