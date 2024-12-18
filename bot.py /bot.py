import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# التوكن الخاص بالبوت
BOT_TOKEN = "7891692862:AAGKGmIJubgxLkKELRMSdxpMXgm-QBooqM0"
bot = telebot.TeleBot(BOT_TOKEN)

# روابط القنوات
CHANNELS = [
    {"name": "القناة الأولى", "url": "https://t.me/+VxJLVxgndBo0Zjk0"},
    {"name": "القناة الثانية", "url": "https://t.me/+HqqRgjQZYjpmMDVk"},
    {"name": "القناة الثالثة", "url": "https://t.me/+LFhCUR0ASBtmZmE8"}
]

# رابط بوت الأرقام
NUMBERS_BOT_LINK = "https://t.me/ALBERUBOT?start=Y9SF1G3A"

# الرسائل الترحيبية باللغتين
MESSAGES = {
    "ar": """
✧･ﾟ: *✧･ﾟ:* ✨✨  
🎉 *مرحباً بك في بوت الخدمات الخاص بنا!* 🎉  
✨✨ *:･ﾟ✧*:･ﾟ✧ ✨✨  

⚠️ *لاستخدام هذا البوت، يُرجى الاشتراك في القنوات المطلوبة أولاً.*  
📌 بعد الاشتراك، اضغط على زر "تحقق من الاشتراك" للمتابعة.  
🎯 *نحن هنا لخدمتك دائمًا!*  
    """,
    "en": """
✧･ﾟ: *✧･ﾟ:* ✨✨  
🎉 *Welcome to our service bot!* 🎉  
✨✨ *:･ﾟ✧*:･ﾟ✧ ✨✨  

⚠️ *To use this bot, please subscribe to the required channels first.*  
📌 After subscribing, click the "Verify Subscription" button to proceed.  
🎯 *We're always here to serve you!*  
    """
}

# التحقق من الاشتراك
def check_subscription(user_id):
    for channel in CHANNELS:
        try:
            status = bot.get_chat_member(chat_id=channel["url"], user_id=user_id)
            if status.status not in ['member', 'administrator', 'creator']:
                return False
        except Exception:
            return False
    return True

# نقطة البداية
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    user_lang = message.from_user.language_code  # تحديد لغة المستخدم
    lang = "en" if user_lang == "en" else "ar"

    # تجهيز الرسالة الترحيبية
    welcome_message = MESSAGES[lang]

    # إنشاء الأزرار
    markup = InlineKeyboardMarkup()
    for channel in CHANNELS:
        markup.add(InlineKeyboardButton(f"📢 {channel['name']}", url=channel["url"]))

    markup.add(InlineKeyboardButton("✅ تحقق من الاشتراك", callback_data="check_subscription"))
    bot.send_message(chat_id=message.chat.id, text=welcome_message, reply_markup=markup, parse_mode="Markdown")

# التحقق من الاشتراك عند الضغط على الزر
@bot.callback_query_handler(func=lambda call: call.data == "check_subscription")
def callback_check_subscription(call):
    user_id = call.from_user.id
    if check_subscription(user_id):
        bot.answer_callback_query(callback_query_id=call.id, text="✅ تم التحقق بنجاح!" if call.from_user.language_code != "en" else "✅ Verified successfully!")
        bot.send_message(chat_id=call.message.chat.id, text="🎉 شكراً لاشتراكك! يمكنك الآن الذهاب إلى بوت الأرقام." if call.from_user.language_code != "en" else "🎉 Thank you for subscribing! You can now access the numbers bot.")
        
        # زر الانتقال إلى بوت الأرقام
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🔢 الذهاب إلى بوت الأرقام", url=NUMBERS_BOT_LINK))
        bot.send_message(chat_id=call.message.chat.id, text="👇 اضغط الزر أدناه 👇" if call.from_user.language_code != "en" else "👇 Click the button below 👇", reply_markup=markup)
    else:
        bot.answer_callback_query(callback_query_id=call.id, text="❌ لم يتم الاشتراك بجميع القنوات." if call.from_user.language_code != "en" else "❌ Not all channels subscribed.")
        bot.send_message(chat_id=call.message.chat.id, text="⚠️ يرجى الاشتراك في جميع القنوات المطلوبة ثم الضغط على زر *تحقق من الاشتراك*." if call.from_user.language_code != "en" else "⚠️ Please subscribe to all required channels and click the *Verify Subscription* button.")

# تشغيل البوت
bot.polling()


