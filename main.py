import telebot
from telebot import types
import google.generativeai as genai

# መረጃዎች
TOKEN = '8513514659:AAFEWJ647fRyfNhasIvT-IyJDJR5gD5an-8'
API_KEY = 'AIzaSyBRFThyLfz94J__xxzoWJ6qJcaKYF9pCtc'
ADMIN_ID = '7266453062'

# AI Setup
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')
bot = telebot.TeleBot(TOKEN)

# ዋናው ሜኑ (ሁሉንም የያዘ)
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
    text = "✨ *እንኳን ወደ AA COMPANY Smart Bot በደህና መጡ!* ✨\n\nሁሉንም አገልግሎቶች በአንድ ላይ እዚህ ያገኛሉ። ምን ልርዳዎት?"
    bot.send_message(message.chat.id, text, reply_markup=get_main_menu(), parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    chat_id = call.message.chat.id
    
    if call.data == "ai_mode":
        msg = bot.send_message(chat_id, "🤖 *የ AI ሞድ በርቷል!* ማንኛውንም ጥያቄ ይጻፉልኝ (ለምሳሌ፦ የፊዚክስ ጥያቄ ወይም ስለ ቴክኖሎጂ)።")
        bot.register_next_step_handler(msg, handle_ai_chat)
    
    elif call.data == "about_aa":
        bot.send_message(chat_id, "🏢 *AA COMPANY*፦ በትምህርት፣ በቴክኖሎጂ እና በፈጠራ ላይ ያተኮረ ተቋም ነው።")
    
    elif call.data == "formulas":
        formula_text = "📐 *ጠቃሚ ፎርሙላዎች*፦\n\n• Force: $F = m \cdot a$\n• Circle Area: $A = \pi r^2$\n• Velocity: $v = d/t$"
        bot.send_message(chat_id, formula_text, parse_mode="Markdown")

    elif call.data == "passive_income":
        income = "💰 *ተገቢ ገቢ*፦ በዲጂታል አማራጮች (እንደ App ማበልጸግ እና ሰርቬይ) ገቢ ማግኘት የሚቻልባቸውን መንገዶች እንጠቁማለን።"
        bot.send_message(chat_id, income)

    elif call.data == "ask_question":
        msg = bot.send_message(chat_id, "❓ ጥያቄዎን ይጻፉ፣ ለአስተዳዳሪው ይደርሳል።")
        bot.register_next_step_handler(msg, forward_to_admin)

    bot.answer_callback_query(call.id)

# 1. AI የሚመልስበት ክፍል
def handle_ai_chat(message):
    bot.send_chat_action(message.chat.id, 'typing')
    try:
        response = model.generate_content(message.text)
        bot.reply_to(message, response.text, reply_markup=get_main_menu())
    except:
        bot.reply_to(message, "ይቅርታ፣ AIው አሁን ስራ በዝቶበታል።", reply_markup=get_main_menu())

# 2. ጥያቄን ወደ አንተ ማስተላለፊያ
def forward_to_admin(message):
    user_info = f"👤 ከ: {message.from_user.first_name}\n🆔 ID: {message.from_user.id}"
    question = f"📩 *አዲስ ጥያቄ መጥቷል*፦\n\n{message.text}\n\n{user_info}"
    bot.send_message(ADMIN_ID, question, parse_mode="Markdown")
    bot.send_message(message.chat.id, "✅ ጥያቄዎ ደርሷል። በቅርቡ እንመልስልዎታለን!", reply_markup=get_main_menu())

# 3. አንተ ለጥያቄው "Reply" ስታደርግ ለተጠቃሚው እንዲደርስ (ያልተቀነሰ)
@bot.message_handler(func=lambda message: message.reply_to_message is not None and str(message.chat.id) == ADMIN_ID)
def reply_to_user(message):
    try:
        original_msg = message.reply_to_message.text
        target_user_id = original_msg.split("ID: ")[1].strip()
        reply_text = f"📩 *ከ AA COMPANY የተላከ መልስ*፦\n\n{message.text}"
        bot.send_message(target_user_id, reply_text, parse_mode="Markdown")
        bot.reply_to(message, "✅ መልስዎ ለተጠቃሚው ደርሷል።")
    except Exception:
        bot.reply_to(message, "❌ ስህተት፡ መልሱን መላክ አልተቻለም።")

if __name__ == "__main__":
    print("AA Smart Bot (Full AI Version) is running...")
    bot.infinity_polling()
