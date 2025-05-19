from aiogram import html, Router, types, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from db.models import User, Group, Social

main_router = Router()


async def check_membership(bot, user_id: int, group_id: int) -> bool:
    try:
        member = await bot.get_chat_member(chat_id=group_id, user_id=user_id)
        return member.status in ["member", "administrator", "creator"]
    except Exception as e:
        print(f"⚠️ Error checking membership for group {group_id}: {str(e)}")
        return False


@main_router.message(CommandStart())
async def command_start_handler(message: Message, bot) -> None:
    user_id = message.from_user.id
    user = await User.exists_user(id_=user_id)
    if not user:
        await User.create(id=user_id, username=message.from_user.username)

    groups = await Group.get_all_column()
    socials = await Social.get_all_url()

    keyboard_builder = InlineKeyboardBuilder()
    non_subscribed_count = 0

    for group in groups:
        is_member = await check_membership(bot, user_id, group.id)
        if not is_member:
            button_text = group.title if group.title else f"📢 Group {group.id}"
            keyboard_builder.button(
                text=button_text,
                url=group.url,
                callback_data=f"group_{group.id}"
            )
            non_subscribed_count += 1

    for social in socials:
        keyboard_builder.button(
            text="🔗 Click",
            url=social.url,
        )

    response = f"👋 Assalomu alaykum, {html.bold(message.from_user.full_name)}!\n\n"
    if non_subscribed_count > 0:
        response += f"📢 Iltimos, quyidagi {non_subscribed_count} ta kanallarga obuna bo‘ling:\n\n"
        keyboard_builder.button(
            text="✅ Tekshirish",
            callback_data="check_membership"
        )
    else:
        response += "🎉 Siz barcha kerakli kanallarga obuna bo‘lgansiz!\n\n"

    keyboard_builder.adjust(1)

    await message.answer(
        text=response,
        reply_markup=keyboard_builder.as_markup(),
        disable_web_page_preview=True
    )


@main_router.callback_query(F.data == "check_membership")
async def process_check_membership(callback: CallbackQuery, bot) -> None:
    user_id = callback.from_user.id
    groups = await Group.get_all_column()

    keyboard_builder = InlineKeyboardBuilder()
    non_subscribed_count = 0
    response = "🔍 Obuna holati:\n\n"

    for group in groups:
        is_member = await check_membership(bot, user_id, group.id)
        group_title = group.title or f"📢 Group {group.id}"
        group_url = group.url
        status = "✅ Obuna bo‘lgansiz" if is_member else "❌ Obuna bo‘lmagansiz"
        response += f"{group_title}: {status}\n"

        if not is_member:
            keyboard_builder.button(
                text=group_title,
                url=group_url,
                callback_data=f"group_{group.id}"
            )
            non_subscribed_count += 1

    if non_subscribed_count > 0:
        keyboard_builder.button(
            text="✅ Tekshirish",
            callback_data="check_membership"
        )
        response += f"\n⚠️ Iltimos, yuqoridagi {non_subscribed_count} ta kanarga obuna bo‘ling."
    else:
        response += "\n🎉 Rahmat! Siz barcha kanallarga obuna bo‘lgansiz."

    keyboard_builder.adjust(1)

    current_text = callback.message.text

    if current_text != response:
        await callback.message.edit_text(
            text=response,
            reply_markup=keyboard_builder.as_markup() if non_subscribed_count > 0 else None
        )
    await callback.answer()


@main_router.callback_query(F.data.startswith("group_"))
async def process_group_button(callback: types.CallbackQuery) -> None:
    group_id = int(callback.data.split("_")[1])
    group = await Group.get(group_id)

    if group:
        response = f"📢 Kanal: {group.title}"
        if group.url:
            response += f"\n🔗 Havola: {group.url}"
        await callback.answer(response, show_alert=True)
    else:
        await callback.answer(text="⚠️ Kanal topilmadi", show_alert=True)
