import asyncio
import logging
import sys

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand

from bot.dispacher import TOKEN
from bot.handlers import dp


# from bot.middilwares import all_middleware
# from aiogram.utils.i18n import I18n
# i18n = I18n(path="locales", default_locale="en", domain="messages")

async def set_bot_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Botni ishga tushiradi."),
        BotCommand(command="/admin", description="Faqat admin uchun.")
    ]
    await bot.set_my_commands(commands=commands)


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    # await bot.delete_webhook()
    await set_bot_commands(bot)
    # await all_middleware(dp, i18n)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
