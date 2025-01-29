from aiogram.fsm.state import State, StatesGroup


class Training(StatesGroup):
    exists_training = State()


class AddingCards(StatesGroup):
    adding_word = State()
    adding_translation = State()
