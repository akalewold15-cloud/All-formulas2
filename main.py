import telebot
from telebot import types
import google.generativeai as genai

# --- ኮንፊገሬሽን ---
TOKEN = '8513514659:AAFEWJ647fRyfNhasIvT-IyJDJR5gD5an-8'
API_KEY = 'AIzaSyBRFThyLfz94J__xxzoWJ6qJcaKYF9pCtc'
ADMIN_ID = '7266453062'

# --- Gemini AI Setup ---
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

bot = telebot.TeleBot(TOKEN)

# --- የዋና ሜኑ አዝራሮች ---
def get_main_menu():
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_ai = types.InlineKeyboardButton("🤖 በ AI ጠይቅ", callback_data="ai_mode")
    btn_about = types.InlineKeyboardButton("🏢 ስለ AA COMPANY", callback_data="about_aa")
    btn_formula = types.InlineKeyboardButton("📐 ፎርሙላዎች", callback_data="formulas")
    btn_income = types.InlineKeyboardButton("💰 ተገቢ ገቢ (Income)", callback_data="passive_income")
    btn_ask = types.InlineKeyboardButton("❓ ጥያቄ ለመጠየቅ", callback_data="ask_question")
    btn_channel = types.InlineKeyboardButton("📢 Join Channel", url="https://t.me/smart_kihilot")
    
    markup.add(btn_ai, btn_about, btn_formula, btn_income, btn_ask, btn_channel)
    return markup

# --- Start Handler ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "✨ *እንኳን ወደ AA COMPANY Smart Bot በደህና መጡ!* ✨\n\n"
        "እውቀት፣ ቴክኖሎጂ እና አርቲፊሻል ኢንተለጀንስን በአንድ ላይ ያገኛሉ።\n"
        "ምን ልርዳዎት? ከታች ካሉት አማራጮች ይምረጡ፦"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=get_main_menu(), parse_mode="Markdown")

# --- Button Handlers ---
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    chat_id = call.message.chat.id
    
    if call.data == "ai_mode":
        msg = bot.send_message(chat_id, "🤖 *የ AI ሞድ በርቷል!*\nማንኛውንም ጥያቄ ይጻፉልኝ፣ Gemini AI ይመልስልዎታል።\n(ለመውጣት 'exit' ይበሉ)")
        bot.register_next_step_handler(msg, handle_ai_chat)
        
    elif call.data == "about_aa":
        bot.send_message(chat_id, "🏢 *AA COMPANY*፦ የቴክኖሎጂ ፈጠራዎችን እና የትምህርት ጥራትን ለማሳደግ የሚሰራ ተቋም ነው።")
        
    elif call.data == "formulas":
        formula_text = (
            "📐 *ጠቃሚ የትምህርት ፎርሙላዎች*፦\n\n"
            "• *Force*: $F = m \cdot a$\n"
            "• *Circle Area*: $A = \pi r^2$\n"
            "• *Quadratic*: $x = \\frac{-b \pm \sqrt{b^2 - 4ac}}{2a}$"
        )
        bot.send_message(chat_id, formula_text, parse_mode="Markdown")

    elif call.data == "passive_income":
        income_text = "💰 *ተገቢ ገቢ (Passive Income)*፦\nበመስመር ላይ ገንዘብ የሚገኝባቸውን ህጋዊ መንገዶች እና የዲጂታል ክህሎቶችን እዚህ እናሳውቃለን።"
        bot.send_message(chat_id, income_text)

    elif call.data == "ask_question":
        msg = bot.send_message(chat_id, "❓ *ጥያቄዎን ይጻፉልኝ።* በቀጥታ ለአስተዳዳሪው ይደርሳል።")
        bot.register_next_step_handler(msg, forward_to_admin)

    bot.answer_callback_query(call.id)

# --- 1. የ Gemini AI Chat Logic ---
def handle_ai_chat(message):
    if message.text.lower() in ['exit', 'ወጣ', '/start', 'back']:
        bot.send_message(message.chat.id, "ከ AI ሞድ ወጥተዋል።", reply_markup=get_main_menu())
        return

    bot.send_chat_action(message.chat.id, 'typing')
    try:
        response = model.generate_content(message.text)
        if response.text:
            bot.reply_to(message, response.text)
        else:
            bot.reply_to(message, "ይቅርታ፣ መልስ ማግኘት አልቻልኩም።")
    except Exception as e:
        bot.reply_to(message, "⚠️ AIው ለጊዜው አልሰራም። እባክዎ ትንሽ ቆይተው ይሞክሩ።")
    
    # ለተከታታይ AI ውይይት እንደገና Register እናደርጋለን
    msg = bot.send_message(message.chat.id, "ሌላ ጥያቄ ካለዎት ይቀጥሉ (ለመውጣት 'exit' ይበሉ)፦")
    bot.register_next_step_handler(msg, handle_ai_chat)

# --- 2. ጥያቄን ለ Admin ማስተላለፍ ---
def forward_to_admin(message):
    user_info = f"👤 ከ: {message.from_user.first_name}\n🆔 ID: {message.from_user.id}"
    question_payload = f"📩 *አዲስ ጥያቄ መጥቷል*፦\n\n{message.text}\n\n{user_info}"
    
    bot.send_message(ADMIN_ID, question_payload, parse_mode="Markdown")
    bot.send_message(message.chat.id, "✅ ጥያቄዎ ለ AA COMPANY ደርሷል። በቅርቡ እንመልስልዎታለን!", reply_markup=get_main_menu())

# --- 3. Admin ለተጠቃሚው Reply ሲያደርግ ---
@bot.message_handler(func=lambda message: message.reply_to_message is not None and str(message.chat.id) == ADMIN_ID)
def reply_to_user(message):
    try:
        original_text = message.reply_to_message.text
        # ID-ውን ከመልእክቱ ውስጥ ፈልጎ ማውጣት
        target_id = original_text.split("ID: ")[1].strip()
        
        reply_body = f"📩 *ከ AA COMPANY የተላከ መልስ*፦\n\n{message.text}"
        bot.send_message(target_id, reply_body, parse_mode="Markdown")
        bot.reply_to(message, "✅ መልስዎ ለተጠቃሚው ደርሷል።")
    except Exception as e:
        bot.reply_to(message, "❌ ስህተት፡ መልሱን መላክ አልተቻለም። (ID አልተገኘም)")

# --- Bot ን ማስነሳት ---
if __name__ == "__main__":
    print("AA Smart Bot (AI Integrated) ስራ ጀምሯል...")
    bot.infinity_polling()
