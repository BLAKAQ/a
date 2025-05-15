import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from AnonXMusic import app
from config import OWNER_ID, START_IMG_URL
from AnonXMusic.utils.database import get_served_chats, get_served_users

# شكل الرسالة الجديد
MESSAGE = f"""
<b>🎶 بوت الموسيقى الأسطوري على تيليجرام 🎶</b>

⚡️ <b>أداء خرافي</b> بدون تقطيع أو توقف  
🔊 <b>صوت نقي وجودة عالية</b>  
🛠️ <b>مزود بمميزات حصرية وخدمات متقدمة</b>

📌 فقط ارفع البوت "أدمن" في مجموعتك أو قناتك  
🔥 واستمتع بأفضل تجربة موسيقية في المحادثات الصوتية

───────────────
🤖 <b>اسم البوت:</b> <code>@{app.username}</code>  
🎧 <b>لتشغيل الأغاني بالمحادثات الصوتية مباشرة</b>

━━━━━━━━━━━━━━
<b>⬇️ اضغط الزر أدناه لإضافة البوت الآن</b>
"""

# زر الإضافة
BUTTON = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("➕ اضف البوت إلى مجموعتك / قناتك", url=f"https://t.me/{app.username}?startgroup=True")
        ]
    ]
)

# دالة إرسال الرسالة
async def send_message_to_chats_and_users():
    try:
        chats = await get_served_chats()
        for chat_info in chats:
            chat_id = chat_info.get("chat_id")
            if isinstance(chat_id, int):
                try:
                    await app.send_photo(
                        chat_id,
                        photo=START_IMG_URL,
                        caption=MESSAGE,
                        reply_markup=BUTTON,
                        parse_mode="html"
                    )
                    await asyncio.sleep(1)
                except Exception:
                    continue

        users = await get_served_users()
        for user_info in users:
            user_id = user_info.get("user_id")
            if isinstance(user_id, int):
                try:
                    await app.send_photo(
                        user_id,
                        photo=START_IMG_URL,
                        caption=MESSAGE,
                        reply_markup=BUTTON,
                        parse_mode="html"
                    )
                    await asyncio.sleep(1)
                except Exception:
                    continue
    except Exception:
        pass

# أمر التحكم من قبل المالك
@app.on_message(filters.command(["اعلان للبوت"], "") & filters.user(OWNER_ID))
async def auto_broadcast_command(client: Client, message: Message):
    await message.reply("📢 جاري إرسال الإعلان إلى جميع المجموعات والقنوات والمستخدمين...")
    await send_message_to_chats_and_users()
    await message.reply("✅ تم إرسال الإعلان بنجاح إلى الجميع.")
