import telebot
from telebot import types

TOKEN = '8513514659:AAFEWJ647fRyfNhasIvT-IyJDJR5gD5an-8'
# የአንተን ID እዚህ ጋር ተካው (ጥያቄዎች ወደ አንተ እንዲመጡ)
ADMIN_ID = '7266453062'

bot = telebot.TeleBot(TOKEN)

# ዋናው ሜኑ
def get_main_menu():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🏢 ስለ AA COMPANY", callback_data="about_aa"),
        types.InlineKeyboardButton("📐 ፎርሙላዎች", callback_data="formulas"),
        types.InlineKeyboardButton("💡 የፈጠራ ምክሮች", callback_data="creative_tips"),
        types.InlineKeyboardButton("🌌 ጠፈርና ሳይንስ", callback_data="science"),
        types.InlineKeyboardButton("💰 ተገቢ ገቢ (Passive Income)", callback_data="passive_income"),
        types.InlineKeyboardButton("❓ ጥያቄ ለመጠየቅ", callback_data="ask_question"),
        types.InlineKeyboardButton("📢 Join Channel", url="https://t.me/smart_kihilot")
    )
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(
        message.chat.id, 
        "🚀 *እንኳን ወደ AA COMPANY መጡ!*\nእውቀትና ፈጠራ የሚገናኙበት ማዕከል። ምን እንርዳዎት?", 
        reply_markup=get_main_menu(), 
        parse_mode="Markdown"
    )

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    chat_id = call.message.chat.id
    
    if call.data == "about_aa":
        bot.send_message(chat_id, "🏢 *AA COMPANY*፦ በትምህርት፣ በቴክኖሎጂ እና በፈጠራ ላይ ያተኮረ ተቋም ነው።")
    
    elif call.data == "creative_tips":
        tips = ("💡 *የፈጠራ ምክሮች*፦\n"
                "• ሁልጊዜ 'ለምን?' ብለህ ጠይቅ።\n"
                "• ትናንሽ ስህተቶች የትልቅ ግኝት መጀመሪያ ናቸው።\n"
                "• በየቀኑ ቢያንስ 15 ደቂቃ አዲስ ነገር አንብብ።")
        bot.send_message(chat_id, tips, parse_mode="Markdown")

    elif call.data == "science":
        science = ("🌌 *ጠፈርና ሳይንስ*፦\n"
                   "• የኳንተም ፊዚክስ ስለ ትናንሽ ቅንጣቶች ሚስጥር ይነግረናል።\n"
                   "• በሰማይ ላይ የምናያቸው ከዋክብት የብዙ ሺህ ዓመታት የብርሃን ጉዞ ውጤቶች ናቸው።")
        bot.send_message(chat_id, science, parse_mode="Markdown")

    elif call.data == "passive_income":
        income = ("💰 *ተገቢ ገቢ*፦\n"
                  "• ዲጂታል ክህሎቶችን ማዳበር ለወደፊት ገቢ መሰረት ነው።\n"
                  "• አፕሊኬሽኖችን እና የኦንላይን እድሎችን በጥንቃቄ መመርመር ይጠቅማል።")
        bot.send_message(chat_id, income, parse_mode="Markdown")

    elif call.data == "ask_question":
        msg = bot.send_message(chat_id, "❓ *ጥያቄዎን አሁን ይጻፉልኝ።* በቀጥታ ለባለሙያዎቻችን ይደርሳል።")
        bot.register_next_step_handler(msg, forward_to_admin)

    bot.answer_callback_query(call.id)

# ጥያቄን ወደ አንተ ማስተላለፊያ
def forward_to_admin(message):
    user_info = f"👤 ከ: {message.from_user.first_name} (@{message.from_user.username})\n🆔 ID: {message.from_user.id}"
    question = f"📩 *አዲስ ጥያቄ መጥቷል*፦\n\n{message.text}\n\n{user_info}"
    
    # ወደ አንተ ይላካል
    bot.send_message(ADMIN_ID, question, parse_mode="Markdown")
    # ለተጠቃሚው ማረጋገጫ ይሰጠዋል
    bot.send_message(message.chat.id, "✅ ጥያቄዎ ደርሶናል። በቅርቡ መልስ እንሰጥዎታለን!", reply_markup=get_main_menu())

if __name__ == "__main__":
    bot.infinity_polling()
