from aiogram import types
from aiogram.dispatcher import FSMContext
from data.config import ADMINS

from loader import dp, db, wallet
from keyboards.inline import inline_buttons
from utils.misc.button_indicator import indicator


@dp.message_handler(commands='idadm', chat_id = ADMINS)
async def cmd_admin(message: types.Message, state: FSMContext):
    my_balance = wallet.balance()
    users_sum = db.get_sum_balance()
    profit = my_balance - users_sum

    await message.answer(
        "<b>Средства проекта</b>\n"
        f"<b>- Общий:</b> <code>{my_balance}₽</code>\n"
        f"<b>- Пользователи:</b> <code>{users_sum}₽</code>\n"
        f"<b>- Прибыль:</b> <code>{profit}₽</code>",
            reply_markup=inline_buttons.admin()
    )