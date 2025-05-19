import asyncio

from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.handlers.functions import IsAdmin, get_options_keyboard, MediaStates, get_all_users, get_confirmation_keyboard

media = Router()


@media.message(F.text == "📷 Rasm/Video + Matn", IsAdmin())
async def media_handler(message: Message, state: FSMContext):
    await state.set_state(MediaStates.media)
    await message.answer("📸 Iltimos, yubormoqchi bo'lgan rasm yoki videoni jo'nating.")


@media.message(MediaStates.media, IsAdmin())
async def catch_media_handler(message: Message, state: FSMContext):
    if message.photo:
        media_id = message.photo[-1].file_id
        media_type = "photo"
    elif message.video:
        media_id = message.video.file_id
        media_type = "video"
    else:
        await message.answer("⚠️ Iltimos, rasm yoki video yuboring.")
        return

    await state.update_data(media_id=media_id, media_type=media_type)
    await state.set_state(MediaStates.text)
    await message.answer(
        "✍️ Mediya bilan birga yuboriladigan matnni kiriting yoki faqat mediya jo‘natish uchun /skip bosing.")


@media.message(MediaStates.text, IsAdmin())
async def catch_text_handler(message: Message, state: FSMContext):
    if message.text == "/skip":
        text = ""
    else:
        text = message.text

    await state.update_data(text=text)
    await state.set_state(MediaStates.confirmation)
    await message.answer("✅ Matn qabul qilindi.")
    await message.answer(
        text="📢 Ushbu mediyani foydalanuvchilarga yubormoqchimisiz?",
        reply_markup=await get_confirmation_keyboard()
    )


@media.message(MediaStates.confirmation)
async def send_media_handler(message: Message, state: FSMContext, bot: Bot):
    if message.text.lower() == "✅ ha":
        data = await state.get_data()
        media_id = data.get("media_id")
        media_type = data.get("media_type")
        caption = data.get("text", "")
        user_ids = await get_all_users()

        if not user_ids:
            await message.answer("⚠️ Hozircha foydalanuvchilar mavjud emas.")
            return

        await state.clear()
        count = 0
        tasks = []

        for user_id in user_ids:
            try:
                if media_type == "photo":
                    tasks.append(bot.send_photo(chat_id=user_id, photo=media_id, caption=caption))
                elif media_type == "video":
                    tasks.append(bot.send_video(chat_id=user_id, video=media_id, caption=caption))

                count += 1
                if count % 28 == 0:
                    await asyncio.gather(*tasks)
                    tasks = []
                    await asyncio.sleep(1)
            except Exception as e:
                print(f"⚠️ Xatolik user id {user_id}: {e}")

        if tasks:
            await asyncio.gather(*tasks)

        await message.answer(
            text="✅ Media barcha foydalanuvchilarga muvaffaqiyatli yuborildi! 🎉",
            reply_markup=await get_options_keyboard()
        )

    elif message.text.lower() == "❌ yo‘q":
        await state.clear()
        await message.answer(
            text="🚫 Media yuborilmadi. Jarayon bekor qilindi.",
            reply_markup=await get_options_keyboard()
        )

    else:
        await message.answer("⚠️ Iltimos, «✅ Ha» yoki «❌ Yo‘q» tugmasini bosing.")
