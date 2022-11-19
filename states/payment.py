from aiogram.dispatcher.filters.state import State, StatesGroup


class WithDraw(StatesGroup):
	step1 = State()
	step2 = State()
	step3 = State()


class TopUp(StatesGroup):
    step1 = State()
    step2 = State()
    step3 = State()