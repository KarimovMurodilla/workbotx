import random
import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp, db, wallet, p2p
from utils.misc.qiwi import Payment
from data.config import QIWI_NUMBER
from states.payment import WithDraw, TopUp
from keyboards.inline import inline_buttons
from keyboards.default import keyboard_buttons




@dp.message_handler(state="*", text = 'Отмена')
async def cancel_handler(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Отменено!", reply_markup=keyboard_buttons.main_menu())

    
# Эхо хендлер, куда летят текстовые сообщения без указанного состояния
@dp.message_handler(text = "Личный кабинет")
async def home(message: types.Message):
    user_id = message.from_user.id
    balance = db.get_user_balance(user_id)

    await message.answer_photo(
        photo = 'AgACAgIAAxkBAAINXWN3iq0AAbtaS7hZLIxrXL-MfIBH-QACMMExGxc6sUrZu_TK8G6PPAEAAwIAA3kAAysE',
        caption  =  f"Ваш баланс: <code>{balance}₽</code>\n\n"
                    "- Вы пригласили: <code>1ч</code>\n"
                    "  Заработали: <code>0.2₽</code>\n\n"
                    "Пригласительная ссылка\n"
                    f"└ <a href='https://t.me/teeessstbot?start={message.from_user.id}'>Зажмите чтоб скопировать</a>",
        reply_markup=inline_buttons.payment()
    )


# ----WithDraw---
@dp.callback_query_handler(lambda c: c.data == 'withdraw')
async def callback_withdraw(c: types.CallbackQuery, state: FSMContext):
    user_id = c.from_user.id
    balance = db.get_user_balance(user_id)
    
    if balance > 0.0:
        await c.answer()
        await WithDraw.step1.set()
        await c.message.answer("На  какую сумму Вы хотите сделать вывод?", 
            reply_markup = keyboard_buttons.cancel())
    
    else:
        await c.answer(show_alert = True, text = "⚠️ Ошибка:\n\n"
						"У вас недостаточно средств")


@dp.message_handler(state = WithDraw.step1)
async def home(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    balance = db.get_user_balance(user_id)
    
    if message.text.isdigit():
        if int(message.text) <= balance:
            async with state.proxy() as data:
                data['user_money'] = message.text
                
                await WithDraw.step2.set()
                await message.answer("Отправьте мне номер карты для вывода средства на ней.")
        else:
            await message.answer("⚠️ Ошибка:\n\n"
								 "У вас недостаточно средств")
    else:
        await message.answer("⚠️ Ошибка:\n\n"
							 "Вводите только цифрами!")


@dp.message_handler(state = WithDraw.step2)
async def home(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        user_id = message.from_user.id
        recipient = message.text
        user_money = data['user_money']
        comment = (f"{user_id}_{random.randint(1000, 9999)}")
        
        prv_id = Payment.get_card_system(recipient)
        payment_data = {'sum': user_money,
                        'to_card': recipient,
                        'prv_id': prv_id}
        answer_from_qiwi = Payment.send_to_card(payment_data)
        
        try:
            status_transaction = answer_from_qiwi["transaction"]["state"]
            if status_transaction['code'] == "Accepted":
                today = datetime.datetime.today()
                fee_with_commission = int(user_money)+int(user_money)/100*2+50
                balance = db.get_user_balance(user_id)
                new_balance = balance - fee_with_commission
                db.update_balance(user_id, new_balance)
                await message.answer("🔔 Уведомление:\n\nВаша заявка принята в обработку!\nОжидайте перевода в течении 24х часов.")
        
        except Exception as e:
            print(answer_from_qiwi)
            print(e, type(e))
            await message.answer("⚠️ Ошибка:\n\n"
				"Пожалуйста проверьте карта/номер получателя !")
            
            await state.finish()



# ----Top Up----
@dp.callback_query_handler(lambda c: c.data == 'top_up')
async def callback_top_up(c: types.CallbackQuery, state: FSMContext):
	await c.answer()

	await TopUp.step1.set()
	await c.message.answer("Отправьте сумму на которую хотите пополнить баланс.", 
			reply_markup = keyboard_buttons.cancel())
	

@dp.message_handler(state=TopUp.step1)
async def process_top_up(message: types.Message, state: FSMContext):
    
    if message.text.isdigit():
        user_id = message.from_user.id
        user_money = int(message.text)
        comment = (f"{user_id}_{random.randint(1000, 9999)}")
        bill = p2p.bill(amount=user_money, lifetime=15, comment=comment)
        
        await message.answer(f"<b>Информация об оплате\nК зачислению:</b> <code>{float(message.text)} ₽</code>", 
            reply_markup = inline_buttons.show_payment(bill_id = bill.bill_id, url = bill.pay_url, price = user_money))
        await state.finish()
    
    else:
        await message.answer("Введите цифрами!")


@dp.callback_query_handler(lambda c: c.data.startswith('check_'))
async def check_payment(c: types.CallbackQuery, state: FSMContext):
    try:
        user_id = c.from_user.id
        ids = c.data[6:].split(',')
        bill = ids[0]
        price = ids[1]
        today = datetime.datetime.today()
        
        if str(p2p.check(bill_id = bill).status) == "PAID":
            balance = db.get_user_balance(user_id)
            new_balance = balance + int(price)
            db.update_balance(user_id, new_balance)
            
            await c.message.delete()
            await c.answer(show_alert = True, text = "🔔 Уведомление:\n\nПоздравляю, оплата прошла успешно!")
            
            await c.message.answer("Главное меню", reply_markup = keyboard_buttons.main_menu())
            await state.finish()
        
        else:
            await c.answer(show_alert = True, text = "❗️Вы не оплатили счет!")
    
    except Exception as e:
        print(e)
        await c.answer()
        await c.message.answer("Произошла неизвестная ошибка или утекли срок данных. Пожалуйста повторите попытку!")



# @dp.message_handler(state="*", content_types=types.ContentTypes.PHOTO)
# async def photo(message: types.Message):
#     print(message.photo[-1].file_id)