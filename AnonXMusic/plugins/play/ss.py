import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import FloodWait
import traceback

from AnonXMusic import app
from config import OWNER_ID, START_IMG_URL
from AnonXMusic.utils.database import (
    get_served_chats,
    get_served_users,
)

# رسالة الإعلان
MESSAGE = f"""- اقوي بوت ميوزك قنوات و جروبات سرعه وجوده خارقه

وبدون تهنيج او تقطيع او توقف وكمان ان البوت في مميزات جامدة⚡️♥️.

ارفع البوت ادمن فقناتك او جروبك واستمتع بجوده الصوت و السرعه الخياليه للبوت ⚡️♥️

معرف البوت 🎸 [ @{app.username} ]

➤ 𝘉𝘰𝘵 𝘵𝘰 𝘱𝘭𝘢𝘺 𝘴𝘰𝘯𝘨𝘴 𝘪𝘯 𝘷𝘰𝘪𝘤e 𝘤𝘩𝘢𝘵 ♩🎸 \n\n-𝙱𝙾𝚃 ➤ @{app.username}"""

# زر دعوة البوت
BUTTON = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("اضف البوت الي مجموعتك او قناتك ❤️✨", url=f"https://t.me/{app.username}?startgroup=True")
        ]
    ]
)

# دالة إرسال الرسالة
async def send_message_to_chats_and_users():
    try:
        chats = await get_served_chats()
        print(f"🔹 عدد الكروبات: {len(chats)}")
        for chat_info in chats:
            chat_id = chat_info.get('chat_id')
            if isinstance(chat_id, int):
                try:
                    await app.send_photo(chat_id, photo=START_IMG_URL, caption=MESSAGE, reply_markup=BUTTON)
                    print(f"✅ تم الإرسال إلى الكروب: {chat_id}")
                    await asyncio.sleep(1)
                except FloodWait as e:
                    print(f"⚠️ FloodWait {e.value} ثانية - الانتظار...")
                    await asyncio.sleep(e.value)
                except Exception as e:
                    print(f"❌ خطأ في كروب {chat_id} -> {e}")
                    traceback.print_exc()

        users = await get_served_users()
        print(f"🔸 عدد المستخدمين: {len(users)}")
        for user_info in users:
            user_id = user_info.get('user_id')
            if isinstance(user_id, int):
                try:
                    await app.send_photo(user_id, photo=START_IMG_URL, caption=MESSAGE, reply_markup=BUTTON)
                    print(f"✅ تم الإرسال إلى المستخدم: {user_id}")
                    await asyncio.sleep(1)
                except FloodWait as e:
                    print(f"⚠️ FloodWait {e.value} ثانية - الانتظار...")
                    await asyncio.sleep(e.value)
                except Exception as e:
                    print(f"❌ خطأ في مستخدم {user_id} -> {e}")
                    traceback.print_exc()

    except Exception as e:
        print(f"❌ خطأ عام في دالة الإرسال: {e}")
        traceback.print_exc()

# دالة تنفيذ الأمر "اعلان للبوت"
@app.on_message(filters.command(["اعلان للبوت"], "") & filters.user(OWNER_ID))
async def auto_broadcast_command(client: Client, message: Message):
    print("🚀 استلم البوت الأمر بنجاح من المالك.")
    await message.reply("✅ تم بدء نشر الإعلان في جميع المجموعات والمستخدمين، يرجى الانتظار...")
    await send_message_to_chats_and_users()
    await message.reply("✅ تم الانتهاء من إرسال الإعلان لجميع المجموعات والمستخدمين.")
