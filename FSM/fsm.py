from aiogram.fsm.state import State, StatesGroup

class AdminAddState(StatesGroup):
    tg_id = State()

class AdminDelState(StatesGroup):
    tg_id = State()

class CategoryState(StatesGroup):
    name = State()
    cat_type = State()

class BookState(StatesGroup):
    title = State()
    description = State()
    image = State()
    cat_fk = State()
    doc = State()

    book_file = State()

class HistoryQuestionState(StatesGroup):
    question = State()

class QuestionAnswer(StatesGroup):
    user_id = State()
    scientist = State()
    answer = State()