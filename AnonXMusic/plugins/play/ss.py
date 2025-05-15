import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from AnonXMusic import app
from config import OWNER_ID, START_IMG_URL
from AnonXMusic.utils.database import (
    get_served_chats,
    get_served_users,
)

# الرسالة بشكل عرض احترافي وجذاب
MESSAGE = f"""
🎧 **أقوى بوت تشغيل موسيقى على تيليجرام**

💥 سرعة خارقة | 🔊 جودة صوت عالية  
💡 مميزات حصرية وبدون أي تقطيع أو تهنيج

🛡️ قم برفع البوت كـ "أدمن" في مجموعتك أو قناتك  
📌 واستمتع بتجربة لا مثيل لها في تشغيل الأغاني داخل المحادثات الصوتية

──────────────
🤖 اسم البوت: [ @{app.username} ]  
🎶 بوت لتشغيل الأغاني في المحادثات الصوتية

━━━━━━━━━━━━━━
🔗 اضغط الزر بالأسفل لإضافة البوت
"""

# الزر
BUTTON = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("➕ اضف البوت لمجموعتك أو قناتك", url=f"https://t.me/{app.username}?startgroup=True")
        ]
    ]
)

# دالة النشر
async def send_message_to_chats_and_users():
    try:
        chats = await get_served_chats()
        for chat_info in chats:
            chat_id = chat_info.get('chat_id')
            if isinstance(chat_id, int):
                try:
                    await app.send_photo(chat_id, photo=START_IMG_URL, caption=MESSAGE, reply_markup=BUTTON)
                    await asyncio.sleep(1)
                except Exception:
                    continue
        users = await get_served_users()
        for user_info in users:
            user_id = user_info.get('user_id')
            if isinstance(user_id, int):
                try:
                    await app.send_photo(user_id, photo=START_IMG_URL, caption=MESSAGE, reply_markup=BUTTON)
                    await asyncio.sleep(1)
                except Exception:
                    continue
    except Exception:
        pass

# أمر النشر عند إرسال الأمر من المالك
@app.on_message(filters.command(["اعلان للبوت"], "") & filters.user(OWNER_ID))
async def auto_broadcast_command(client: Client, message: Message):
    await message.reply("🚀 جارٍ إرسال الإعلان إلى جميع الجروبات والقنوات والمستخدمين...")
    await send_message_to_chats_and_users()
    await message.reply("✅ تم الانتهاء من إرسال الإعلان بنجاح.")
