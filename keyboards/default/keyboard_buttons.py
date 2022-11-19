from aiogram import types


def main_menu():
    menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Объявление")
    btn2 = types.KeyboardButton("Подробнее")
    btn3 = types.KeyboardButton("Личный кабинет")
    menu.add(btn1, btn2)
    menu.add(btn3)

    return menu


def cancel():
    menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn = types.KeyboardButton("Отмена")
    menu.add(btn)

    return menu