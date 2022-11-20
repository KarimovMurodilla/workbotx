import os

from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp
from states.process_captcha import ProcessCaptcha
from utils.misc.captcha.generator import CaptchaPhoto



@dp.callback_query_handler(lambda c: c.data == 'subscribed', state="*")
async def cancel_handler(c: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await c.message.delete()
    captcha = CaptchaPhoto()
    captcha.generate_captcha()

    with open(captcha.path, 'rb') as photo:
        await c.message.answer_photo(
            photo,
            caption="⚠️ Чтоб продолжить использовать бота, Вам необходимо решить капчу.", 
            reply_markup=types.ReplyKeyboardRemove()
        )
        os.remove(captcha.path)
    
    async with state.proxy() as data:
        data['captcha_key'] = captcha.key

    await ProcessCaptcha.step1.set()