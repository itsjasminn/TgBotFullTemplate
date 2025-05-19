from bot.dispacher import dp
from bot.handlers.comments import controller
from bot.handlers.get_group_id import channel
from bot.handlers.main_handler import main_router
from bot.handlers.medias import media
from bot.handlers.words import word

dp.include_routers(*[
    main_router,
    controller,
    channel,
    media,
    word
])
