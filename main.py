import telebot
import time

# ያንተ ቦት Token (በቀጥታ ገብቷል)
TOKEN = '8513514659:AAFEWJ647fRyfNhasIvT-IyJDJR5gD5an-8'
bot = telebot.TeleBot(TOKEN)

# ቦቱ ሲጀመር የሚላክ ሰላምታ
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "ሰላም! 🚀 እንኳን ወደ AA COMPANY መጡ። እኔ የእርስዎ ብልህ የዲጂታል ረዳት ነኝ። ምን ልርዳዎት?")

# ለጥያቄዎች በቁምነገር እንዲመልስ
@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    chat_id = message.chat.id
    user_text = message.text.lower()

    # የማሰብ ምልክት (Processing)
    bot.send_chat_action(chat_id, 'typing')
    time.sleep(1.5) # ቦቱ እያሰበ እንዲመስል

    if "ፎርሙላ" in user_text or "math" in user_text:
        response = ("የሂሳብ እና የፊዚክስ ፎርሙላዎች የአጽናፈ ዓለሙ መግለጫዎች ናቸው። "
                    "ለጥያቄዎ ትክክለኛውን ፎርሙላ በዝርዝር ለማቅረብ ዝግጁ ነኝ።")
    elif "ስለ aa" in user_text:
        response = ("AA COMPANY የተመሰረተው የቴክኖሎጂ እና የትምህርት ጥራትን ለማሳደግ ነው። "
                    "የእኛ ግብ መረጃን ወደ እውቀት መቀየር ነው።")
    elif "አመሰግናለሁ" in user_text:
        response = "ምንም አይደል! የ AA COMPANY ስኬት የኔም ስኬት ነው። በሌላ በምን ላግዝህ?"
    else:
        response = ("ጥያቄዎ ትኩረቴን ስቧል። ይህንን ጉዳይ በባለሙያ ደረጃ ለመተንተን "
                    "እባክዎ ጥያቄዎን በግልጽ ያስቀምጡልኝ።")

    bot.send_message(chat_id, response)

# ቦቱ ያለማቋረጥ እንዲሰራ
if __name__ == "__main__":
    print("AA Smart Bot ስራ ጀምሯል...")
    bot.infinity_polling()
