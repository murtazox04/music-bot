from aiogram.dispatcher.filters.state import StatesGroup, State


class GetState(StatesGroup):
    next = State()
    back = State()
    end = State()
