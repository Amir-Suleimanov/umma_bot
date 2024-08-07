from database.engine import session_maker
from database.models import User, Category, Book, Admin
from sqlalchemy import select


async def set_user(tg_id) -> None:
    """
    Записать нового юзера в бд если его не существует
    """
    
    async with session_maker() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        
        if not user:
            session.add(User(tg_id = tg_id))
            await session.commit()


async def set_admin(tg_id):
    """
    Записать нового админа в бд если его не существует
    """
    
    async with session_maker() as session:
        admin = await session.scalar(select(Admin).where(Admin.tg_id == tg_id))
        
        if not admin:
            session.add(Admin(tg_id = tg_id))
            await session.commit()
            return True
        
        return False

async def delete_admin(tg_id):
    """
    Удалить админа из бд
    """
    
    async with session_maker() as session:
        admin = await session.scalar(select(Admin).where(Admin.tg_id == tg_id))
        
        if admin:
            session.delete(admin)
            await session.commit()
            return True
        
        return False

async def check_user_admin(tg_id):
    """
    Проверка, является ли пользователь администратором
    """
    
    async with session_maker() as session:
        user = await session.scalar(select(Admin).where(Admin.tg_id == tg_id))
        
        if user:
            return True
        
        return False
    

async def create_category(name, cat_type):
    """
    Создать новую категорию
    """
    
    async with session_maker() as session:
        category = await session.scalar(select(Category).where(Category.name == name))

        if not category:
            session.add(Category(name=name, cat_type=cat_type))
            await session.commit()
            return True
        
        return False
        

async def get_cats(cat_type=None):
    """
    Получить все книги по категории
    """
    
    async with session_maker() as session:
        if cat_type: return await session.scalars(select(Category).where(Category.cat_type == cat_type))
        return await session.scalars(select(Category))


async def create_book(title, description, image, cat_id, book_file):
    """
    Создать новую книгу
    """
    
    async with session_maker() as session:
        book = await session.scalar(select(Book).where(Book.title == title))

        if not book:
            session.add(Book(title=title, description=description, image=image, category=cat_id, book_file=book_file))
            await session.commit()
            return True
        
        return False
    

async def get_books_by_cat(book_cat):
    """
    Получить все книги по категории
    """
    
    async with session_maker() as session:
        return await session.scalars(select(Book).where(Book.category == book_cat))
    

async def get_book_by_id(book_id):
    """
    Получить книгу по id
    """
    
    async with session_maker() as session:
        return await session.scalar(select(Book).where(Book.id == book_id))
    

async def delete_book(book_id):
    """
    Удалить книгу из бд
    """
    
    async with session_maker() as session:
        book = await session.scalar(select(Book).where(Book.id == book_id))

        if book:
            await session.delete(book)
            await session.commit()
            return [book.book_file, book.image]
        return False
    
async def delete_category(category_id):
    """
    Удалить категорию из бд
    """
    
    async with session_maker() as session:
        category = await session.scalar(select(Category).where(Category.id == category_id))
        
        if category:
            await session.delete(category)
            await session.commit()
            return True
        
        return False
    

async def all_books(cat_id):
    """
    Получить все книги по категории
    """
    
    async with session_maker() as session:
        return await session.scalars(select(Book).where(Book.category == cat_id))
