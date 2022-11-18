from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware

from data.config import CHANNEL_ID
from loader import bot

class SubscriptionMiddleware(BaseMiddleware):
    """
    Simple middleware
    """

    async def on_process_message(self, message: types.Message, data: dict):
        user = await bot.get_chat_member(CHANNEL_ID, 875587704)

        if not user.is_chat_member():
            await self.send_link(message)
            raise CancelHandler()


    async def send_link(self, message: types.Message):
        await message.reply(f"Присоединяйтесь на наш канал: @WebAppGames")
