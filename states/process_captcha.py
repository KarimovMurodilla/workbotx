from aiogram.dispatcher.filters.state import State, StatesGroup


class ProcessCaptcha(StatesGroup):
	step1 = State()