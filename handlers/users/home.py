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
        await c.message.answer(
            "<b>🔔 Уведомление:</b>\n\n"
            "Вы можете вывести от <code>500</code> до <code>2500</code> руб (За день). Комиссия Qiwi составляет - <code>2% + 50.0 ₽</code>", 
                reply_markup = inline_buttons.continue_btn())
    
    else:
        await c.answer(show_alert = True, text = "⚠️ Ошибка:\n\n"
						"У вас недостаточно средств")


@dp.callback_query_handler(lambda c: c.data == 'continue', state = WithDraw.step1)
async def continue_handler(c: types.CallbackQuery, state: FSMContext):
    await c.message.answer("Отправьте мне сумму которую хотите вывести.")
    await WithDraw.next()


@dp.message_handler(state = WithDraw.step2)
async def process_withdraw_2(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    balance = db.get_user_balance(user_id)
    
    if message.text.isdigit():
        async with state.proxy() as data:
            data['user_money'] = message.text
            
            await WithDraw.step3.set()
            await message.answer("Отправьте мне номер карты для вывода средства на ней.", reply_markup=keyboard_buttons.cancel())
    else:
        await message.answer("⚠️ Ошибка:\n\n"
							 "Вводите только цифрами!")


@dp.message_handler(state = WithDraw.step3)
async def process_withdraw_3(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['recipient'] = message.text
        user_money = data.get('user_money')
    
    fee_with_comission = int(user_money)+int(user_money)/100*2+50

    await message.answer(
        "<b>Информация об выводе</b>\n"
        f"<b>К списанию:</b> <code>{fee_with_comission}₽</code>\n"
        f"<b>К зачислению:</b> <code>{user_money}₽</code>\n"
        f"<b>На:</b> <code>{message.text}</code>",
            reply_markup=inline_buttons.confirm_btn()
    )
    await WithDraw.next()


@dp.callback_query_handler(lambda c: c.data == 'confirm', state = WithDraw.step4)
async def continue_handler(c: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        user_id = c.from_user.id
        recipient = data.get('recipient')
        user_money = data['user_money']
        comment = (f"{user_id}_{random.randint(1000, 9999)}")

        balance = db.get_user_balance(user_id)
        fee_with_commission = int(user_money)+int(user_money)/100*2+50

    if int(fee_with_commission) <= balance:        
        prv_id = Payment.get_card_system(recipient)
        payment_data = {'sum': user_money,
                        'to_card': recipient,
                        'prv_id': prv_id}
        answer_from_qiwi = Payment.send_to_card(payment_data)
        
        try:
            status_transaction = answer_from_qiwi["transaction"]["state"]
            if status_transaction['code'] == "Accepted":
                new_balance = balance - fee_with_commission
                db.update_balance(user_id, new_balance)
                await c.message.answer("🔔 Уведомление:\n\nВаша заявка принята в обработку!\nОжидайте перевода в течении 24х часов.")
        
        except Exception as e:
            print(answer_from_qiwi)
            print(e, type(e))
            await c.message.answer("⚠️ Ошибка:\n\n"
				"Пожалуйста проверьте карта/номер получателя !")
            
            await state.finish()
    else:
        await c.message.answer("⚠️ Ошибка:\n\n"
                            "У вас недостаточно средств")



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
            await c.answer(
                show_alert = True, 
                text  = "⚠️ Ошибка:\n\n" 
                        "Оплата не прошла или же вы не оплатили счёт, повторите попытку или обратитесь в поддержку бота."
            
            )
    
    except Exception as e:
        print(e)
        await c.answer()
        await c.message.answer("Произошла неизвестная ошибка или утекли срок данных. Пожалуйста повторите попытку!")



# @dp.message_handler(state="*", content_types=types.ContentTypes.PHOTO)
# async def photo(message: types.Message):
#     print(message.photo[-1].file_id)