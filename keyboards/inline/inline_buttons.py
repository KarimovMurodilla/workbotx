from aiogram import types


def payment():
    menu = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text="Вывести", callback_data="withdraw")
    btn2 = types.InlineKeyboardButton(text="Пополнить", callback_data="top_up")
    menu.add(btn1, btn2)

    return menu


def show_payment(bill_id, url, price):
	menu_payment = types.InlineKeyboardMarkup(row_width=2)
	link_to_pay = types.InlineKeyboardButton(text = "Оплатить", url = url)
	check_payment = types.InlineKeyboardButton(text = "Обновить", callback_data = f"check_{bill_id},{price}")
	menu_payment.add(link_to_pay, check_payment)

	return menu_payment


def subscribed():
    menu = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text="Подписался", callback_data='subscribed')
    