import asyncio
import os

from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram import Bot, Dispatcher, types
# from aiogram.fsm.strategy import FSMStrategy

from dotenv import find_dotenv, load_dotenv
from common.bot_cmds_list import private

# from middlewares.db import DataBaseSession
from database.engine import create_db, drop_db
# from middlewares.db import CounterMiddleware

from handlers.user_private import user_pr_router
from handlers.admin_private import admin_router
from handlers.chat_public import chat_router

# from handlers.user_gr import user_gr_router
# from handlers.admin_pr import admin_router


load_dotenv(find_dotenv())

ALLOWED_UPDATES = [
    'message',
    'edited_message',
    'channel_post',
    'edited_channel_post',
    'inline_query',
    'chosen_inline_result',
    'callback_query',
    'shipping_query',
    'pre_checkout_query',
    'poll',
    'poll_answer',
    'my_chat_member',
    'chat_member',
    'chat_join_request'
]

bot = Bot(token=os.getenv("TOKEN"), default=DefaultBotProperties(parse_mode=ParseMode.HTML))

dp = Dispatcher()

dp.include_router(chat_router)
dp.include_router(user_pr_router)
dp.include_router(admin_router)


async def main():
    await create_db()
    # dp.update.middleware(DataBaseSession(session_pool=session_maker))
    await bot.delete_webhook(drop_pending_updates=True)
    # await bot.delete_my_commands(scope=types.BotCommandScopeAllPrivateChats()) чтобы удалять все команды
    await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)
    await drop_db()


if __name__ == '__main__':
    try:
        print('Бот запущен')
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот завершил свою работу')
        