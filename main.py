import telebot
from telebot import types
import os

# Token-ህን እዚህም አስቀምጠነዋል ለደህንነት
TOKEN = '8513514659:AAFEWJ647fRyfNhasIvT-IyJDJR5gD5an-8'
bot = telebot.TeleBot(TOKEN)

def get_main_menu():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🏢 ስለ AA COMPANY", callback_data="about_aa"))
    markup.add(types.InlineKeyboardButton("📐 የትምህርት ፎርሙላዎች", callback_data="formulas"))
    markup.add(types.InlineKeyboardButton("💡 ፈጠራዎች እና ምክሮች", callback_data="tips"))
    markup.add(types.InlineKeyboardButton("📢 Join Channel", url="https://t.me/smart_kihilot"))
    markup.add(types.InlineKeyboardButton("📞 እርዳታ/ጥያቄ", callback_data="help"))
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    text = "✨ *እንኳን ወደ AA COMPANY Smart Bot በደህና መጡ!* ✨\n\nእኛ እውቀትን እና ቴክኖሎጂን እናገናኛለን። ከታች ይምረጡ፡"
    bot.send_message(message.chat.id, text, reply_markup=get_main_menu(), parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "about_aa":
        resp = "🏢 *AA COMPANY* የተመሰረተው የቴክኖሎጂ እና የትምህርት ጥራትን ለማሳደግ ነው።"
    elif call.data == "formulas":
        resp = "📐 *ፎርሙላዎች*፡\n1. ኃይል = m x a\n2. የክበብ ስፋት = πr²"
    elif call.data == "tips":
        resp = "💡 *ጠቃሚ ምክር*፡- በየቀኑ አዲስ ነገር መማር የረጅም ጊዜ ስኬት ምስጢር ነው።"
    elif call.data == "help":
        resp = "📞 *እርዳታ*፡- ጥያቄዎን ይጻፉልኝ፣ የ AA COMPANY ቡድን በቅርቡ ይመልስልዎታል።"
    else:
        resp = "እባክዎን ከሜኑ ውስጥ ይምረጡ።"
    
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, resp, reply_markup=get_main_menu(), parse_mode="Markdown")

# Render ላይ ቦቱ እንዳይዘጋ ይህን በደንብ ይጠቀሙ
if __name__ == "__main__":
    print("Bot is running...")
    bot.polling(none_stop=True)
