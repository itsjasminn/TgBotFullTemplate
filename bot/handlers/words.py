import asyncio

from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.handlers.functions import IsAdmin, get_options_keyboard, TextStates, get_all_users, get_confirmation_keyboard

word = Router()


@word.message(Command("admin"), IsAdmin())
async def word_handler(message: Message):
    await message.answer(
        text="🛠 Iltimos, quyidagi tugmalardan birini tanlang!",
        reply_markup=await get_options_keyboard()
    )


@word.message(F.text == "📝 Matn", IsAdmin())
async def text_handler(message: Message, state: FSMContext):
    await state.set_state(TextStates.text)
    await message.answer("✍️ Yubormoqchi bo'lgan matningizni kiriting:")


@word.message(TextStates.text, IsAdmin())
async def catch_text_handler(message: Message, state: FSMContext):
    if len(message.text) > 4096:
        await message.answer("⚠️ Matn juda uzun! Iltimos, 4096 ta belgidan kamroq yozing.")
        return

    await state.update_data(text=message.text)
    await state.set_state(TextStates.confirmation)
    await message.answer("✅ Matn qabul qilindi.")
    await message.answer(
        "📢 Matnni foydalanuvchilarga yubormoqchimisiz?",
        reply_markup=await get_confirmation_keyboard()
    )


@word.message(TextStates.confirmation)
async def send_text_handler(message: Message, state: FSMContext, bot: Bot):
    if message.text.lower() == "✅ ha":
        data = await state.get_data()
        text = data.get("text")
        user_ids = await get_all_users()

        if not user_ids:
            await message.answer("⚠️ Hozircha foydalanuvchilar mavjud emas.")
            return

        await state.clear()
        count = 0
        tasks = []

        for user_id in user_ids:
            try:
                tasks.append(bot.send_message(chat_id=user_id, text=text))
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
            text="✅ Matn barcha foydalanuvchilarga muvaffaqiyatli yuborildi! 🎉",
            reply_markup=await get_options_keyboard()
        )

    elif message.text.lower() == "❌ yo‘q":
        await state.clear()
        await message.answer(
            text="🚫 Matn yuborilmadi. Jarayon bekor qilindi.",
            reply_markup=await get_options_keyboard()
        )

    else:
        await message.answer("⚠️ Iltimos, «✅ Ha» yoki «❌ Yo‘q» tugmasini bosing.")
