from aiogram import Router, F, Bot
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from db.models import Group

controller = Router()
GROUP_CHAT_ID = -1002310173087
restricted_users = set()
before_sent = set()


async def check_subscription(user_id, bot):
    required_chats = await Group.get_group_ids()
    print(f"📢 Talab qilinadigan chatlar: {required_chats}")
    for chat_id in required_chats:
        try:
            member = await bot.get_chat_member(chat_id=chat_id, user_id=user_id)
            if member.status not in ['member', 'administrator', 'creator']:
                print(f"🚫 Foydalanuvchi {user_id} {chat_id} da a'zo emas")
                return False
        except Exception as e:
            print(f"⚠️ Chat a'zoligini tekshirishda xatolik: {e}")
            return False
    return True


@controller.message(F.chat.type == "supergroup", F.chat.id == GROUP_CHAT_ID)
async def controller_group(message: Message, bot: Bot):
    user_id = message.from_user.id
    user = message.from_user

    if len(str(user_id)) == 6:
        return

    if user_id in restricted_users or not await check_subscription(user_id=user_id, bot=bot):
        reply_to_message_id = message.message_id if not message.reply_to_message else message.reply_to_message.message_id
        await message.delete()
        restricted_users.add(user_id)

        keyboard = InlineKeyboardBuilder()
        keyboard.add(
            *[
                InlineKeyboardButton(text="🤖 Botga o'tish", url=f"t.me/{(await bot.get_me()).username}"),
                InlineKeyboardButton(text="✅ Tekshirish", callback_data=f"check_subscription_{user_id}")
            ]
        )
        keyboard.adjust(1)

        reserved_chars = r"""_*[]()~`>#+-=|{}.!"""
        if user.username:
            mention = f"@{user.username}"
        else:
            text = user.full_name
            for char in reserved_chars:
                text = text.replace(char, f"\\{char}")
            mention = f'[{text}](tg://user?id={user_id})'

        message_text = (
            f"👋 {mention}, siz guruhda yozish uchun botga o'tib kanallarga a'zo bo'lishingiz kerak!\n"
            "\n📌 A'zo bo'lib, ✅ Tekshirish tugmasini bosing!"
        )
        for char in reserved_chars:
            message_text = message_text.replace(char, f"\\{char}")

        try:
            if user_id not in before_sent:
                await bot.send_message(
                    chat_id=GROUP_CHAT_ID,
                    text=message_text,
                    reply_markup=keyboard.as_markup(),
                    parse_mode="MarkdownV2",
                    reply_to_message_id=reply_to_message_id
                )
                before_sent.add(user_id)
                print("📩 Xabar muvaffaqiyatli jo'natildi va before_sent ga qo'shildi")
        except Exception as e:
            print(f"❌ Xabar jo'natishda xatolik: {e}")


@controller.callback_query(F.data.startswith("check_subscription_"))
async def check_subscription_callback(callback: CallbackQuery, bot: Bot):
    user_id = callback.from_user.id
    target_user_id = int(callback.data.split("_")[-1])

    if user_id != target_user_id:
        await callback.answer(
            text="⚠️ Bu tugma siz uchun emas!",
            show_alert=True
        )
        return

    if await check_subscription(user_id=user_id, bot=bot):
        restricted_users.discard(user_id)
        before_sent.discard(user_id)
        mention = f'<a href="tg://user?id={user_id}">{callback.from_user.full_name}</a>'
        await callback.message.delete()
        await bot.send_message(
            chat_id=callback.message.chat.id,
            text=f"🎉 ✅ Tabriklaymiz! Endi guruhda yozishingiz mumkin, {mention}",
            parse_mode="HTML"
        )
    else:
        await callback.answer(
            text="🚫 Siz hali barcha kerakli kanallarga a'zo bo'lmadingiz!",
            show_alert=True
        )
