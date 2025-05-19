from typing import List

from aiogram.filters import Filter
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from db.models import Controller, User


class TextStates(StatesGroup):
    text = State()
    confirmation = State()


class MediaStates(StatesGroup):
    media = State()
    text = State()
    confirmation = State()


class IsAdmin(Filter):
    async def __call__(self, message: Message) -> bool:
        return await Controller.exists_admin(message.from_user.id)


async def get_all_users() -> List[int]:
    return await User.get_ids()


async def get_options_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📝 Matn")],
            [KeyboardButton(text="📷 Rasm/Video + Matn")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )


async def get_confirmation_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="✅ Ha"), KeyboardButton(text="❌ Yo‘q")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )