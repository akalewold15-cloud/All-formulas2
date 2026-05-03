import telebot
from google import genai

# --- 1. የራስህን መረጃዎች እዚህ አዘጋጅቻለሁ ---
BOT_TOKEN = "የአንተ_ቴሌግራም_ቦት_ቶክን_እዚህ_ይግባ" # ከ BotFather ያገኘኸው ቶክን
GEMINI_API_KEY = "AIzaSyAbcfnu7CXmfXvjxshiYrxQJJXLIQ4ZxhU" # የሰጠኸኝ API Key
ADMIN_ID = 123456789  # የአንተ ቴሌግራም ID (አማራጭ)

# የቦት እና የ AI ደንበኛ (Client) ማስጀመሪያ
bot = telebot.TeleBot(BOT_TOKEN)
client = genai.Client(api_key=GEMINI_API_KEY)

# --- 2. ቦቱ ሲጀመር (/start) የሚላክ መልዕክት ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # የሚኒ አፑ ሊንክ (ቀደም ብለን የሰራነው Colorful HTML ሊንክ)
    markup = telebot.types.InlineKeyboardMarkup()
    # ማሳሰቢያ፡ የ 'WEB_APP_URL' ቦታ ላይ የ HTML ፋይልህን የጫንክበትን ሊንክ ተካው
    web_app = telebot.types.WebAppInfo("https://የአንተ_ሊንክ.github.io/") 
    button = telebot.types.InlineKeyboardButton(text="AA Formula Finder ክፈት 🚀", web_app=web_app)
    markup.add(button)
    
    welcome_text = (
        "ሰላም! እንኳን ወደ AA All Formulas ቦት በሰላም መጡ።\n\n"
        "• ማንኛውንም የትምህርት ጥያቄ እዚህ መፃፍ ይችላሉ።\n"
        "• ወይም ከታች ያለውን ቁልፍ ተጭነው 'Mini App' መክፈት ይችላሉ።"
    )
    bot.reply_to(message, welcome_text, reply_markup=markup)

# --- 3. የ AI መልስ አሰጣጥ ሎጂክ ---
@bot.message_handler(func=lambda message: True)
def handle_ai_chat(message):
    try:
        # ቦቱ መልስ እስኪያገኝ 'typing...' እንዲል
        bot.send_chat_action(message.chat.id, 'typing')
        
        # ተጠቃሚው የላከውን ጥያቄ ወደ Gemini መላክ
        # እዚህ ጋር gemini-1.5-flash ሞዴልን እንጠቀማለን (ፈጣን ስለሆነ)
        response = client.models.generate_content(
            model="gemini-1.5-flash", 
            contents=message.text
        )
        
        # AIው የሰጠውን መልስ ለተጠቃሚው መላክ
        bot.reply_to(message, response.text)
        
        # ለአንተ (ለአድሚኑ) ሪፖርት እንዲያደርግ (አማራጭ)
        if message.from_user.id != ADMIN_ID:
            print(f"User {message.from_user.first_name} asked: {message.text}")

    except Exception as e:
        # ስህተት ቢፈጠር ለተጠቃሚው የሚላክ መልዕክት
        error_msg = "ይቅርታ፣ አሁን ላይ መልስ ለመስጠት አልቻልኩም። እባክዎ ትንሽ ቆይተው ይሞክሩ።"
        bot.reply_to(message, error_msg)
        print(f"Error: {e}")

# --- ቦቱን ማስጀመር ---
if __name__ == "__main__":
    print("ቦቱ በተሳካ ሁኔታ ስራ ጀምሯል... ሰላም ለኢትዮጵያ! 🇪🇹")
    bot.infinity_polling()
