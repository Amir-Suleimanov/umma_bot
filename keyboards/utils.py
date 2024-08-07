from typing import List
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

import database.requests as rq

from typing import List
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

from database.models import Book, Category


async def create_category_kb(cat_type:str, row:int, column:int, page:int=0):
    categories = await rq.get_cats(cat_type)
    cats:List[Category] = [i for i in categories]
    len_cat:int = len(cats)
    start_gap:int = page * row*column
    end_gap:int = start_gap + row*column
    if len_cat < end_gap: end_gap = len_cat
    cats:List[Category] = cats[start_gap:end_gap]
    keyboard = InlineKeyboardBuilder()

    if len_cat == 0:
        pass
    else:
        for i in range(row):
            rows = []
            if not cats: break
            for j in range(column):
                if not cats: break
                cat = cats.pop(0)
                rows.append(InlineKeyboardButton(text=cat.name, callback_data=f'category:{cat.id}:{cat_type}:0'))
            keyboard.row(*rows)


    if len_cat <= row*column:
        pass
    elif len_cat > row*column and page == 0:
        keyboard.row( InlineKeyboardButton(text="▶️", callback_data=f"cat_type:{cat_type}:{page+1}") )
    elif len_cat > row*column and page == len_cat//(column*row):
        keyboard.row( InlineKeyboardButton(text="◀️", callback_data=f"cat_type:{cat_type}:{page-1}") )
    else:
        keyboard.row(
            InlineKeyboardButton(text="◀️", callback_data=f"cat_type:{cat_type}:{page-1}"),
            InlineKeyboardButton(text="▶️", callback_data=f"cat_type:{cat_type}:{page+1}")
        )
    
    keyboard.row(InlineKeyboardButton(text="Назад",callback_data="back1"))

    return keyboard.as_markup()


async def create_all_category(row:int, column:int, page:int=0):
    categories = await rq.get_cats()
    cats:List[Category] = [i for i in categories]
    len_cat:int = len(cats)
    start_gap:int = page * row*column
    end_gap:int = start_gap + row*column
    if len_cat < end_gap: end_gap = len_cat
    cats:List[Category] = cats[start_gap:end_gap]
    keyboard = InlineKeyboardBuilder()

    if len_cat == 0:
        pass
    else:
        for i in range(row):
            rows = []
            if not cats: break
            for j in range(column):
                if not cats: break
                cat = cats.pop(0)
                rows.append(InlineKeyboardButton(text=cat.name, callback_data=f'add_book_catFK:{cat.id}'))
            keyboard.row(*rows)


    if len_cat <= row*column:
        pass
    elif len_cat > row*column and page == 0:
        keyboard.row( InlineKeyboardButton(text="▶️", callback_data=f"add_book_page:{page+1}") )
    elif len_cat > row*column and page == len_cat//(column*row):
        keyboard.row( InlineKeyboardButton(text="◀️", callback_data=f"add_book_page:{page-1}") )
    else:
        keyboard.row(
            InlineKeyboardButton(text="◀️", callback_data=f"add_book_page:{page-1}"),
            InlineKeyboardButton(text="▶️", callback_data=f"add_book_page:{page+1}")
        )
    

    return keyboard.as_markup()


async def create_book_kb(cat_type, book_cat, row, column, page=0):
    all_books = await rq.get_books_by_cat(book_cat)
    books:List[Book] = [i for i in all_books]

    len_books:int = len(books)
    start_gap:int = page * row*column
    end_gap:int = start_gap + row*column
    if len_books < end_gap: end_gap = len_books
    
    books:List[Book] = books[start_gap:end_gap]
    
    keyboard = InlineKeyboardBuilder()

    if len_books == 0:
        pass
    else:
        for _ in range(row):
            rows = []
            if not books: break
            for j in range(column):
                if not books: break
                book = books.pop(0)
                rows.append(InlineKeyboardButton(text=book.title, callback_data=f'book:{book.id}'))
            keyboard.row(*rows)

    if len_books <= row*column:
        pass
    elif len_books > row*column and page == 0:
        keyboard.row( InlineKeyboardButton(text="▶️", callback_data=f"category:{book_cat}:{cat_type}:{page+1}") )
    elif len_books > row*column and page == len_books//(column*row):
        keyboard.row( InlineKeyboardButton(text="◀️", callback_data=f"category:{book_cat}:{cat_type}:{page-1}") )
    else:
        keyboard.row(
            InlineKeyboardButton(text="◀️", callback_data=f"category:{book_cat}:{cat_type}:{page-1}"),
            InlineKeyboardButton(text="▶️", callback_data=f"category:{book_cat}:{cat_type}:{page+1}")
        )
    
    keyboard.row(InlineKeyboardButton(text="Назад",callback_data=f"cat_type:{cat_type}:0"))

    return keyboard.as_markup()


async def book_back(book_id, user_id):
    keyboard = InlineKeyboardBuilder()
    keyboard.row(InlineKeyboardButton(text="Получить книгу", callback_data=f"get_book:{book_id}"))
    if await rq.check_user_admin(user_id): keyboard.add(InlineKeyboardButton(text='Удалить книгу', callback_data=f'delete_book:{book_id}'))
    return keyboard.as_markup()


async def all_category_for_del(row:int, column:int, page:int=0):
    categories = await rq.get_cats()
    cats:List[Category] = [i for i in categories]
    len_cat:int = len(cats)
    start_gap:int = page * row*column
    end_gap:int = start_gap + row*column
    if len_cat < end_gap: end_gap = len_cat
    cats:List[Category] = cats[start_gap:end_gap]
    keyboard = InlineKeyboardBuilder()

    if len_cat == 0:
        pass
    else:
        for i in range(row):
            rows = []
            if not cats: break
            for j in range(column):
                if not cats: break
                cat = cats.pop(0)
                rows.append(InlineKeyboardButton(text=cat.name, callback_data=f'del_cat:{cat.id}'))
            keyboard.row(*rows)


    if len_cat <= row*column:
        pass
    elif len_cat > row*column and page == 0:
        keyboard.row( InlineKeyboardButton(text="▶️", callback_data=f"delete_category:{page+1}") )
    elif len_cat > row*column and page == len_cat//(column*row):
        keyboard.row( InlineKeyboardButton(text="◀️", callback_data=f"delete_category:{page-1}") )
    else:
        keyboard.row(
            InlineKeyboardButton(text="◀️", callback_data=f"delete_category:{page-1}"),
            InlineKeyboardButton(text="▶️", callback_data=f"delete_category:{page+1}")
        )

    return keyboard.as_markup()