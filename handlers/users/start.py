import os

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp, db
from keyboards.default import keyboard_buttons
from states.process_captcha import ProcessCaptcha
from utils.misc.captcha.generator import CaptchaPhoto


@dp.message_handler(CommandStart(), state='*')
async def bot_start(message: types.Message, state: FSMContext):
    await state.finish()
    captcha = CaptchaPhoto()
    captcha.generate_captcha()

    with open(captcha.path, 'rb') as photo:
        await message.answer_photo(photo, reply_markup=types.ReplyKeyboardRemove())
        os.remove(captcha.path)
    
    async with state.proxy() as data:
        data['captcha_key'] = captcha.key

    await ProcessCaptcha.step1.set()


@dp.message_handler(state=ProcessCaptcha.step1)
async def bot_start(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        captcha_key = data.get('captcha_key')

    if message.text.lower() == captcha_key:
        await message.answer("Добро пожаловать!", reply_markup=keyboard_buttons.main_menu())
        if not db.get_user(message.from_user.id):
            db.reg_user(message.from_user.id)
        await state.finish()

    else:
        await message.answer("Неверно!")