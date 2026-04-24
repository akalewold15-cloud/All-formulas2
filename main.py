import telebot
import time
import os

# TOKEN ን ከ Render Environment Variable እንቀበላለን (ደህንነቱ የተጠበቀ እንዲሆን)
TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(func=lambda message: True)
def smart_bot(message):
    chat_id = message.chat.id
    # እያሰላሰለ መሆኑን ያሳያል
    bot.send_message(chat_id, "🔍 እባክዎን ይጠብቁ፣ እየተነተንኩ ነው...")
    time.sleep(1.5) 

    text = message.text.lower()
    
    if "ፎርሙላ" in text or "math" in text:
        response = ("የሂሳብ እና የፊዚክስ ፎርሙላዎች የአጽናፈ ዓለሙ መግለጫዎች ናቸው። "
                    "ለጥያቄዎ ትክክለኛውን ፎርሙላ እያቀረብኩ ነው...")
    elif "ስለ aa" in text:
        response = ("AA COMPANY የተመሰረተው የቴክኖሎጂ እና የትምህርት ጥራትን ለማሳደግ ነው። "
                    "የእኛ ግብ መረጃን ወደ እውቀት መቀየር ነው።")
    else:
        response = ("ጥያቄዎ ትኩረቴን ስቧል። ይህንን ጉዳይ በባለሙያ ደረጃ ለመመለስ፣ "
                    "እባክዎ ጥያቄዎን በግልጽ ያስቀምጡልኝ።")
    
    bot.reply_to(message, response)

if __name__ == "__main__":
    bot.infinity_polling()
