from aiogram import F, Bot, types, Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.enums.parse_mode import ParseMode
from os import remove

from filters.chat_types import ChatTypeFilter
from keyboards import reply
import database.requests as rq
from FSM.fsm import AdminAddState, AdminDelState, CategoryState, BookState
from keyboards.utils import create_all_category, all_category_for_del


"""
Обработка админ панели
"""

admin_router = Router()
admin_router.message.filter(ChatTypeFilter(["private"]))

# Админка
@admin_router.message(F.text.lower() == "/admin")
async def admin(message: types.Message) -> None:
    if message.from_user.id in (1511191966,) or await rq.check_user_admin(message.from_user.id):
        await message.answer("Выберите действие", reply_markup=reply.admin_kb)

    else: await message.answer("Недостаточно прав")


@admin_router.callback_query(F.data == "add_admin")
async def add_admin(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id in (1511191966,) or await rq.check_user_admin(callback.from_user.id):
        await state.set_state(AdminAddState.tg_id)
        await callback.message.answer("Введите id пользователя которого хотите добавить в администраторы")
    else:
        await callback.message.answer("Недостаточно прав")
    await callback.answer() 



@admin_router.message(AdminAddState.tg_id)
async def add_admin_tg_id(message: types.Message, state: FSMContext):
    admin = await rq.set_admin(message.text)
    await state.clear()
    
    if admin: await message.answer('Пользователь теперь администратор')
    else: await message.answer('Пользователь уже администратор')
    


@admin_router.callback_query(F.data == 'delete_admin')
async def delete_admin(callback: CallbackQuery, state: FSMContext):
    if await rq.check_user_admin(callback.from_user.id):
        await state.set_state(AdminDelState.tg_id)
        await callback.message.answer("Введите id пользователя которого хотите удалить из администраторов")
    else:
        await callback.message.answer("Недостаточно прав")
    await callback.answer() 
    

@admin_router.message(AdminDelState.tg_id)
async def delete_admin_tg_id(message: types.Message, state: FSMContext):
    admin = await rq.delete_admin(message.text)
    await state.clear()
    
    if admin: await message.answer('Пользователь удален из администраторов')
    else: await message.answer('Пользователь не найден в администраторах')

# Добавление категории
@admin_router.callback_query(F.data == 'create_category')
async def create_category(callback: CallbackQuery, state: FSMContext):
    if await rq.check_user_admin(callback.from_user.id):
        await state.set_state(CategoryState.name)
        
        await callback.message.answer("Введите название категории")
    
    else: await callback.message.answer("Недостаточно прав")
    await callback.answer() 



@admin_router.message(CategoryState.name)
async def create_category_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(CategoryState.cat_type)
    data = await state.get_data()
    
    await message.answer(
        '''Выберите тип, к которой относится ваша категория из следующего списка:\n <code>Об Исламе</code>, <code>История Дагестана</code>, <code>История Ислама</code>''',
        parse_mode=ParseMode.HTML)


@admin_router.message(CategoryState.cat_type)
async def create_category_cat_type(message: types.Message, state: FSMContext):
    
    if message.text.lower() not in ["об исламе", "история дагестана", "история ислама"]:
        await message.answer('Выберите один из предложенных вариантов')
        await state.set_state(CategoryState.cat_type)
    else:
        data = await state.get_data()
        await state.clear()

        name = message.text.lower()
        if name == "об исламе": category = await rq.create_category(data['name'], 'Islam')
        elif name == "история дагестана": category = await rq.create_category(data['name'], 'Dagestan History')
        elif name == "история ислама": category = await rq.create_category(data['name'], 'Islamic History')

        if category: await message.answer('Категория создана')
        else: await message.answer('Такая категория уже создана')

# Добавление книги
@admin_router.callback_query(F.data == 'add_book')
async def add_book(callback: CallbackQuery, state: FSMContext):
    if await rq.check_user_admin(callback.from_user.id):
        await state.set_state(BookState.title)
        await callback.message.answer("Введите название книги")
    else: await callback.message.answer("Недостаточно прав")
    await callback.answer() 


@admin_router.message(BookState.title)
async def add_book_title(message: types.Message, state: FSMContext):
    if not message.text:
        await message.answer("Вы ввели не название, попробуйте снова")
        await state.set_state(BookState.title)
    else:
        await state.update_data(title=message.text)
        await state.set_state(BookState.image)
        await message.answer("Отправьте изображение книги")

@admin_router.message(BookState.image)
async def add_book_image(message: types.Message, state: FSMContext, bot: Bot):
    try:
        photo, doc_photo='', ''

        if message.photo: photo = message.photo[-1]
        else: doc_photo = message.document
    except:
        await message.answer("Это не изображение, попробуйте снова")
        await state.set_state(BookState.image)
        return
    if photo:
        await state.update_data(image=photo.file_id, doc=photo)
        await state.set_state(BookState.description)
        await message.answer("Добавьте описание")
    elif doc_photo:
        await state.update_data(image=doc_photo.file_name, doc=doc_photo)
        await state.set_state(BookState.description)
        await message.answer("Добавьте описание")
    


@admin_router.message(BookState.description)
async def add_book_description(message: types.Message, state: FSMContext):
    if not message.text:
        await message.answer("Вы ввели не описание, попробуйте снова")
        await state.set_state(BookState.description)
    else:
        await state.update_data(description=message.text)
        await state.set_state(BookState.cat_fk)

        kb =  await create_all_category(
            row=3, column=3
        )
        await message.answer("Выберите категорию к которой относится ваша книга", reply_markup=kb)


@admin_router.callback_query(BookState.cat_fk)
async def add_book_category(callback: CallbackQuery, state: FSMContext):
    if not callback.data.startswith('add_book_catFK:'):
        if callback.data.startswith('add_book_page:'):
            page = int(callback.data.split(':')[1])
            await state.set_state(BookState.cat_fk)
            kb = await create_all_category(row=3, column=3, page=page)
            await callback.message.edit_text("Выберите категорию к которой относится ваша книга", reply_markup=kb)
    else:
        await state.update_data(cat_fk=int(callback.data.split(':')[1]))
        await state.set_state(BookState.book_file)
        await callback.message.edit_text("Отправьте файл книги")
    await callback.answer() 
    

@admin_router.message(BookState.book_file)
async def add_book_file(message: types.Message, state: FSMContext, bot: Bot):
    if message.document:
        document = message.document
        path = f"./media/books/{document.file_name}"
        
        data = await state.get_data()
        photo = data["image"]
        book = await rq.create_book(
            title=data['title'],
            description=data['description'],
            image=data['image'],
            cat_id=data['cat_fk'],
            book_file=path
        )
        await state.clear()

        if book:
            await bot.download(data['doc'], destination=f"./media/photos/{photo}")
            await bot.download(file=document,destination=path)
            await message.answer("Книга создана")
        else: await message.answer("Такая книга уже создана",)
    
        

@admin_router.callback_query(F.data.startswith('delete_book'))
async def delete_book(callback: CallbackQuery, bot: Bot):
    if await rq.check_user_admin(callback.from_user.id):
        book_id = int(callback.data.split(':')[1])
        book = await rq.delete_book(book_id)
        
        if book: 
            remove(book[0])
            remove(f'./media/photos/{book[1]}')
            await callback.message.delete()
            await callback.message.answer("Книга удалена")
        else: await callback.message.answer("Книга не найдена")
    else: await callback.message.answer("Недостаточно прав")
    await callback.answer()


@admin_router.callback_query(F.data.startswith('delete_category:'))
async def delete_category(callback: CallbackQuery):
    if await rq.check_user_admin(callback.from_user.id):
        page = int(callback.data.split(':')[1])
        kb = await all_category_for_del(row=3, column=3, page=page)

        await callback.message.edit_text("Выберите категорию для удаления", reply_markup=kb)
    else: await callback.message.answer("Недостаточно прав")
    await callback.answer()

@admin_router.callback_query(F.data.startswith('del_cat:'))
async def delete_category(callback: CallbackQuery):
    if await rq.check_user_admin(callback.from_user.id):
        cat_id = int(callback.data.split(':')[1])

        books = [i for i in await rq.all_books(cat_id=cat_id)]
        print(books)
        for book in books:
            del_book = await rq.delete_book(book.id)
            print(del_book)
            remove(del_book[0])
            remove(f'./media/photos/{del_book[1]}')
        await rq.delete_category(cat_id)
        await callback.message.edit_text("Все книги в этой категории удалены")
        await callback.message.answer("Категория удалена")
    else: await callback.message.answer("Недостаточно прав")
    await callback.answer()