from aiogram import Dispatcher
from aiogram.utils.i18n import FSMI18nMiddleware


async def all_middleware(dp: Dispatcher, i18n):
    dp.message.middleware(FSMI18nMiddleware(i18n))
