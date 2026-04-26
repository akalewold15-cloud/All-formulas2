import telebot
from telebot import types

TOKEN = '8513514659:AAFEWJ647fRyfNhasIvT-IyJDJR5gD5an-8'
bot = telebot.TeleBot(TOKEN)

# ዋናው ሜኑ (ከ Emoji ጋር)
def get_main_menu():
    markup = types.InlineKeyboardMarkup()
    markup.row(types.InlineKeyboardButton("🏢 ስለ AA COMPANY", callback_data="about_aa"))
    markup.row(types.InlineKeyboardButton("📐 የትምህርት ፎርሙላዎች", callback_data="formulas"))
    markup.row(types.InlineKeyboardButton("💡 ፈጠራዎች እና ምክሮች", callback_data="tips"))
    markup.row(types.InlineKeyboardButton("📢 Join Channel", url="https://t.me/smart_kihilot"))
    markup.row(types.InlineKeyboardButton("📞 እርዳታ/ጥያቄ", callback_data="help"))
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "✨❤ *እንኳን ወደ AA COMPANY Smart Bot በደህና መጡ!* ✨\n\n"
        "እኛ እውቀትን እና ቴክኖሎጂን እናገናኛለን። ከታች ካሉት አማራጮች ውስጥ ይምረጡ፡"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=get_main_menu(), parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "about_aa":
        response = "🏢 *AA COMPANY* የተመሰረተው የቴክኖሎጂ እና የትምህርት ጥራትን ለማሳደግ ነው። የእኛ ግብ መረጃን ወደ እውቀት መቀየር ነው።"
    elif call.data == "formulas":
        response = "📐 *የሂሳብ እና ፊዚክስ ፎርሙላዎች*፡\n\n1. ኃይል (Force) = Mass x Acceleration\n2. የክበብ ስፋት = πr²"
    elif call.data == "tips":
        response = "💡 *የዛሬው ጠቃሚ ምክር*፡- በየቀኑ አዲስ ነገር መማር የረጅም ጊዜ ስኬት ምስጢር ነው።"
    elif call.data == "help":
        response = "📞 *እርዳታ*፡- ጥያቄዎን ይጻፉልኝ፣ የ AA COMPANY ቡድን በቅርቡ ይመልስልዎታል።"
    else:
        response = "እባክዎን ከሜኑ ውስጥ ይምረጡ።"

    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, response, reply_markup=get_main_menu(), parse_mode="Markdown")

if __name__ == "__main__":
    print("AA Smart Bot ስራ ጀምሯል...")
    bot.infinity_polling()
