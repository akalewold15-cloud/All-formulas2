import telebot
from telebot import types

TOKEN = '8513514659:AAFEWJ647fRyfNhasIvT-IyJDJR5gD5an-8'
bot = telebot.TeleBot(TOKEN)

# ዋናው ሜኑ (Inline Buttons)
def get_main_menu():
    markup = types.InlineKeyboardMarkup()
    markup.row(types.InlineKeyboardButton("የ AA COMPANY አላማ", callback_data="about_aa"))
    markup.row(types.InlineKeyboardButton("የትምህርት ፎርሙላዎች", callback_data="formulas"))
    markup.row(types.InlineKeyboardButton("እርዳታ/ጥያቄ", callback_data="help"))
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, 
                     "እንኳን ወደ AA COMPANY Smart Bot በደህና መጡ! 🚀\nለማገዝ ዝግጁ ነኝ። ከታች ካሉት አማራጮች አንዱን ይምረጡ፡", 
                     reply_markup=get_main_menu())

# የአዝራሮች ስራ (Callback Query Handler)
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "about_aa":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "AA COMPANY የተመሰረተው የቴክኖሎጂ እና የትምህርት ጥራትን ለማሳደግ ነው። የእኛ ግብ መረጃን ወደ እውቀት መቀየር ነው።")
    
    elif call.data == "formulas":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "ሒሳብ የአጽናፈ ዓለሙ ቋንቋ ነው። የትኛውን ፎርሙላ ይፈልጋሉ? (ለምሳሌ፦ የፊዚክስ፣ የሒሳብ፣ ወዘተ)")
    
    elif call.data == "help":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "ለበለጠ መረጃ እባክዎ ጥያቄዎን ይጻፉልኝ፣ የ AA COMPANY ባለሙያዎች በቅርቡ ይረዱዎታል።")

    # ከጨረሰ በኋላ ወደ ሜኑ እንዲመለስ
    bot.send_message(call.message.chat.id, "ሌላ ማገልገል እችላለሁ?", reply_markup=get_main_menu())

if __name__ == "__main__":
    print("AA Smart Bot (Modern Edition) ስራ ጀምሯል...")
    bot.infinity_polling()
