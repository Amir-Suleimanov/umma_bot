from aiogram import F, Bot, types, Router
from aiogram.types import CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

from filters.chat_types import ChatTypeFilter
from keyboards import reply
import database.requests as rq
from keyboards.utils import create_category_kb, create_book_kb, book_back
from FSM.fsm import HistoryQuestionState


user_pr_router = Router()
user_pr_router.message.filter(ChatTypeFilter(["private"]))


@user_pr_router.message(CommandStart())
@user_pr_router.message(F.text.lower() == "старт")
async def start_cmd(message: types.Message) -> None:
    await rq.set_user(message.from_user.id)
    await message.answer("вот сюда приветственный текст надо (арабский распознается без проблем вроде)",
                         reply_markup=reply.start_kb)


@user_pr_router.callback_query(F.data == 'history_question')
async def history_question(callback: CallbackQuery):
    await callback.message.answer('Пока в разработке...')



@user_pr_router.message(Command("about"))
async def about(message: types.Message) -> None:
    await message.answer("чота нада про бота написать или убрать эту кнопку?")


@user_pr_router.message(Command("menu"))
async def menu_f(message: types.Message) -> None:
    await message.answer("Какого типа книга вас интересует?", reply_markup=reply.main_menu_kb)


@user_pr_router.callback_query(F.data == "for_menu")
@user_pr_router.callback_query(F.data == "back1")
@user_pr_router.callback_query(F.data == "back2")
@user_pr_router.callback_query(F.data == "back5")
async def for_menu(callback: CallbackQuery):
    await callback.message.edit_text("Какого типа книга вас интересует?", show_alert=True, reply_markup=reply.main_menu_kb)
    await callback.answer() 



@user_pr_router.callback_query(F.data.startswith('cat_type:'))
async def for_cat(callback: CallbackQuery):
    _, cat_type, page = callback.data.split(':')
    reply_markup = await create_category_kb(
        cat_type=cat_type,
        row=3, 
        column=2, 
        page=int(page)
    )
    await callback.message.edit_text("Выберите категорию", reply_markup=reply_markup)
    await callback.answer() 


@user_pr_router.callback_query(F.data.startswith('category:'))
async def for_category(callback: CallbackQuery):
    _, book_cat, cat_type, page = callback.data.split(':')

    kb = await create_book_kb(cat_type=cat_type, book_cat=int(book_cat), row=3, column=3, page=int(page))
    await callback.message.edit_text('Выберите книгу', reply_markup=kb)
    await callback.answer()


@user_pr_router.callback_query(F.data.startswith('book:'))
async def for_book(callback: CallbackQuery):

    _, book_id = callback.data.split(':')
    book = await rq.get_book_by_id(book_id)
    file_path = f'./media/photos/{book.image}'

    kb:types.InlineKeyboardMarkup = await book_back(book_id, callback.from_user.id)
    
    await callback.message.answer_photo(
        photo=types.FSInputFile(path=file_path),
        caption=f"Название: {book.title}\nОписание: {book.description}",
        reply_markup=kb
    )
    await callback.answer()


@user_pr_router.callback_query(F.data.startswith('get_book'))
async def get_book(callback: CallbackQuery, bot: Bot):
    _, book_id = callback.data.split(':')
    book = await rq.get_book_by_id(book_id)
    await bot.send_document(
        chat_id=callback.from_user.id,
        document=types.FSInputFile(book.book_file)
        )
    await callback.answer()


