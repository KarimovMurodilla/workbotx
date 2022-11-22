from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware

from data.config import CHANNEL_ID
from loader import db
from keyboards.inline.inline_buttons import subscribed

class SubscriptionMiddleware(BaseMiddleware):
    """
    Checker subscription chat middleware
    """

    # async def on_process_message(self, message: types.Message, data: dict):
    #     if message.chat.type != 'private':
    #         raise CancelHandler()




    async def on_pre_process_update(self, update: types.Update, data: dict):
        user = None

        if update.callback_query:
            if update.callback_query.message.chat.type != 'private':
                raise CancelHandler()
            user = update.callback_query.from_user


            if update.callback_query.data == 'withdraw' and db.get_status('Вывести') == '❌':
                await update.callback_query.answer("Данная функция не работает!", show_alert=True)
                raise CancelHandler()

            elif update.callback_query.data == 'top_up' and db.get_status('Пополнить') == '❌':
                await update.callback_query.answer("Данная функция не работает!", show_alert=True)
                raise CancelHandler()

        elif update.message:
            if update.message.chat.type != 'private':
                raise CancelHandler()
            user = update.message.from_user

        if user is None:
            return
        
        status = await update.bot.get_chat_member(CHANNEL_ID, user.id)

        if not status.is_chat_member():
            if update.callback_query:
                await update.callback_query.answer("Вы не подписаны!", show_alert=True)
            else:
                await update.message.answer(f"Присоединяйтесь на наш чат: @the_parse_test", reply_markup=subscribed())
            raise CancelHandler()
        
        if update.callback_query:
            await update.callback_query.answer()