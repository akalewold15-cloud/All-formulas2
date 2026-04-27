import telebot
from telebot import types

# ቦት Token እና ያንተ ID
TOKEN = '8513514659:AAFEWJ647fRyfNhasIvT-IyJDJR5gD5an-8'
ADMIN_ID = '7266453062' 

bot = telebot.TeleBot(TOKEN)

# ዋናው ሜኑ (ዘመናዊ አዝራሮች)
def get_main_menu():
    markup = types.InlineKeyboardMarkup(row_width=2)
    item1 = types.InlineKeyboardButton("🏢 ስለ AA COMPANY", callback_data="about_aa")
    item2 = types.InlineKeyboardButton("📐 የትምህርት ፎርሙላዎች", callback_data="formulas")
    item3 = types.InlineKeyboardButton("💡 የፈጠራ ምክሮች", callback_data="creative_tips")
    item4 = types.InlineKeyboardButton("💰 ተገቢ ገቢ (Passive Income)", callback_data="passive_income")
    item5 = types.InlineKeyboardButton("❓ ጥያቄ ለመጠየቅ", callback_data="ask_question")
    item6 = types.InlineKeyboardButton("📢 Join Channel", url="https://t.me/smart_kihilot")
    
    markup.add(item1, item2, item3, item4, item5, item6)
    return markup

# /start ሲባል የሚመጣ ሰላምታ
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "✨ *እንኳን ወደ AA COMPANY Smart Bot በደህና መጡ!* ✨\n\n"
        "እኛ እውቀትን እና ቴክኖሎጂን እናገናኛለን። ምን እንርዳዎት?"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=get_main_menu(), parse_mode="Markdown")

# የአዝራሮች ምላሽ
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    chat_id = call.message.chat.id
    
    if call.data == "about_aa":
        bot.send_message(chat_id, "🏢 *AA COMPANY*፦ በትምህርት፣ በቴክኖሎጂ እና በፈጠራ ላይ ያተኮረ ተቋም ነው።")
    
    elif call.data == "formulas":
        formula_text = (
            "📐 *ጠቃሚ ፎርሙላዎች*፦\n\n"
            "• *Physics*: $F = m \cdot a$\n"
            "• *Math*: $A = \pi r^2$\n"
            "• *Chemistry*: $PV = nRT$"
        )
        bot.send_message(chat_id, formula_text, parse_mode="Markdown")

    elif call.data == "creative_tips":
        tips = "💡 *የፈጠራ ምክር*፦ ትናንሽ ስህተቶች የትልቅ ግኝት መጀመሪያ ናቸው። በየቀኑ አዲስ ነገር ተማር!"
        bot.send_message(chat_id, tips)

    elif call.data == "passive_income":
        income = "💰 *ተገቢ ገቢ*፦ ዲጂታል ክህሎቶችን ማዳበር (ለምሳሌ App ማበልጸግ) ለረጅም ጊዜ ገቢ መሰረት ነው።"
        bot.send_message(chat_id, income)

    elif call.data == "ask_question":
        msg = bot.send_message(chat_id, "❓ *ጥያቄዎን አሁን ይጻፉልኝ።* በቀጥታ ለባለሙያዎቻችን ይደርሳል።")
        bot.register_next_step_handler(msg, forward_to_admin)

    bot.answer_callback_query(call.id)

# ጥያቄን ወደ አንተ (Admin) ማስተላለፊያ
def forward_to_admin(message):
    user_info = f"👤 ከ: {message.from_user.first_name}\n🆔 ID: {message.from_user.id}"
    question = f"📩 *አዲስ ጥያቄ መጥቷል*፦\n\n{message.text}\n\n{user_info}"
    
    bot.send_message(ADMIN_ID, question, parse_mode="Markdown")
    bot.send_message(message.chat.id, "✅ ጥያቄዎ ደርሶናል። በቅርቡ መልስ እንሰጥዎታለን!")

# አንተ ለጥያቄው "Reply" ስታደርግ ለተጠቃሚው እንዲደርስ
@bot.message_handler(func=lambda message: message.reply_to_message is not None and str(message.chat.id) == ADMIN_ID)
def reply_to_user(message):
    try:
        original_msg = message.reply_to_message.text
        # ከተላለፈው መልእክት ውስጥ የላኪውን ID መለየት
        target_user_id = original_msg.split("ID: ")[1].strip()
        
        reply_text = f"📩 *ከ AA COMPANY የተላከ መልስ*፦\n\n{message.text}"
        bot.send_message(target_user_id, reply_text, parse_mode="Markdown")
        bot.reply_to(message, "✅ መልስዎ ለተጠቃሚው ደርሷል።")
    except Exception:
        bot.reply_to(message, "❌ ስህተት፡ መልሱን መላክ አልተቻለም።")

if __name__ == "__main__":
    print("AA Smart Bot is LIVE...")
    bot.infinity_polling()
