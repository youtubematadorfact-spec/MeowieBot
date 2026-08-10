import telebot
import random
import json
import os
import time

TOKEN = "8753752217:AAGfbmrTkGtjSOcyDgGtg5nB2ISEf5s_oD0"
bot = telebot.TeleBot(TOKEN)
DB_FILE = "scores.json"
COOLDOWN_TIME = 300  # ۵ دقیقه به ثانیه

def load_data():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f: return json.load(f)
    return {}

def save_data(data):
    with open(DB_FILE, "w") as f: json.dump(data, f)

# واکنش به کلمات میو یا میویی در گروه
@bot.message_handler(func=lambda message: message.text in ["میو", "میویی", "میو میو"])
def handle_meow(message):
    # این بخش فقط در گروه‌ها کار کند
    if message.chat.type == 'private':
        return

    user_id = str(message.from_user.id)
    user_name = message.from_user.first_name
    current_time = time.time()
    
    data = load_data()
    if user_id not in data:
        data[user_id] = {"points": 0, "last_meow": 0}
    
    last_meow = data[user_id]["last_meow"]
    time_passed = current_time - last_meow
    
    # چک کردن اینکه آیا ۵ دقیقه گذشته است یا خیر
    if time_passed < COOLDOWN_TIME:
        remaining_time = int(COOLDOWN_TIME - time_passed)
        minutes = remaining_time // 60
        seconds = remaining_time % 60
        
        # قالب‌بندی زمان مثل عکس (مثلاً 0:45)
        time_str = f"{minutes}:{seconds:02d}"
        
        warning_msg = f"{user_name}\n\nهنوز میوت نمیاد.. 🐱\nباید {time_str} صب کنی ⏳"
        bot.reply_to(message, warning_msg)
    else:
        # اگر زمان تمام شده بود، امتیاز بده
        points_won = random.randint(1, 15)
        data[user_id]["points"] += points_won
        data[user_id]["last_meow"] = current_time
        save_data(data)
        
        success_msg = f"{user_name}\n\n{points_won} میو پوینت گرفتی 🐾\nمیو پوینت‌هات: {data[user_id]['points']} 💰\nبعد از 5:00 میتوانی دوباره میو میو کنی ⏰"
        bot.reply_to(message, success_msg)

# پیام خوش‌آمدگویی زمان اد شدن به گروه
@bot.message_handler(content_types=['new_chat_members'])
def welcome_to_group(message):
    for member in message.new_chat_members:
        if member.id == bot.get_me().id:
            bot.send_message(message.chat.id, "یه پیشی ناز اینجاست... 🐈\n🐾 شروع کنید به میو میو پیشیا 🐱")

bot.infinity_polling()
      
