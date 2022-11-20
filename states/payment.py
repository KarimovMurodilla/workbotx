from aiogram.dispatcher.filters.state import State, StatesGroup


class WithDraw(StatesGroup):
	step1 = State()
	step2 = State()
	step3 = State()
	step4 = State()
	step5 = State()


class TopUp(StatesGroup):
    step1 = State()
    step2 = State()
    step3 = State()