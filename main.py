import telebot
import google.generativeai as genai
import sqlite3
import math
import datetime
import logging

# --- 1. CONFIGURATION ---
BOT_TOKEN =8513514659:AAFEWJ647fRyfNhasIvT-IyJDJR5gD5an-8
GEMINI_API_KEY = "AIzaSyAbcfnu7CXmfXvjxshiYrxQJJXLIQ4ZxhU"
ADMIN_ID = 7266453062 # Replace with your Telegram ID

# Setup Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Gemini Setup
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Database Setup
def init_db():
    conn = sqlite3.connect('users_data.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                      (id INTEGER PRIMARY KEY, username TEXT, join_date TEXT, last_query TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS history 
                      (user_id INTEGER, query TEXT, response TEXT, timestamp TEXT)''')
    conn.commit()
    conn.close()

init_db()

bot = telebot.TeleBot(BOT_TOKEN)

# --- 2. ADVANCED SCIENTIFIC ENGINE ---
class ScienceEngine:
    @staticmethod
    def solve_quadratic(a, b, c):
        d = (b**2) - (4*a*c)
        if d < 0: return "No real roots"
        sol1 = (-b-math.sqrt(d))/(2*a)
        sol2 = (-b+math.sqrt(d))/(2*a)
        return f"x1: {sol1}, x2: {sol2}"

    @staticmethod
    def star_distance(parallax):
        # Astronomy calculation for distance in parsecs
        if parallax <= 0: return "Invalid parallax"
        return 1 / parallax

# --- 3. BOT HANDLERS ---
@bot.message_handler(commands=['start'])
def welcome(message):
    user_id = message.from_user.id
    username = message.from_user.username
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Save to DB
    conn = sqlite3.connect('users_data.db')
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO users (id, username, join_date) VALUES (?, ?, ?)", (user_id, username, now))
    conn.commit()
    conn.close()

    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    web_app = telebot.types.WebAppInfo("https://your-github-link.github.io/allformulas.html") #
    
    btn1 = telebot.types.InlineKeyboardButton("AA Formula App 🚀", web_app=web_app)
    btn2 = telebot.types.InlineKeyboardButton("Help ❓", callback_data="help")
    markup.add(btn1, btn2)

    bot.send_message(user_id, f"እንኳን ደህና መጡ {message.from_user.first_name}! ይህ 'AA' የተባለው ግዙፍ የቀመር እና የ AI ቦት ነው።", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_ai_request(message):
    user_id = message.from_user.id
    text = message.text

    # Show typing...
    bot.send_chat_action(user_id, 'typing')

    try:
        # Check if user wants a calculation
        if text.startswith("/calc"):
            # Simple logic for quick math
            bot.reply_to(message, f"የስሌት ውጤት: {eval(text.replace('/calc ', ''))}")
            return

        # Gemini AI call
        response = model.generate_content(text)
        reply = response.text

        # Save to History
        conn = sqlite3.connect('users_data.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO history (user_id, query, response, timestamp) VALUES (?, ?, ?, ?)", 
                       (user_id, text, reply, datetime.datetime.now().strftime("%H:%M:%S")))
        conn.commit()
        conn.close()

        bot.reply_to(message, reply)

    except Exception as e:
        logging.error(f"Error: {e}")
        bot.reply_to(message, "ይቅርታ፣ የሆነ ስህተት ተፈጥሯል። ቆይተው ይሞክሩ።")

# --- 4. ADMIN FEATURES ---
@bot.message_handler(commands=['stats'])
def get_stats(message):
    if message.from_user.id == ADMIN_ID:
        conn = sqlite3.connect('users_data.db')
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        count = cursor.fetchone()[0]
        bot.send_message(ADMIN_ID, f"አጠቃላይ ተጠቃሚዎች: {count}")
        conn.close()

if __name__ == "__main__":
    print("AA Mega Bot is running...")
    bot.infinity_polling()
