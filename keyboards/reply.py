from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


start_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Выбрать книгу", callback_data="for_menu")],
        [InlineKeyboardButton(text="Задать вопрос Историку", callback_data="history_question")],
    ],
)


main_menu_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Об Исламе", callback_data="cat_type:Islam:0")],
        [InlineKeyboardButton(text="История Дагестана", callback_data="cat_type:Dagestan History:0")],
        [InlineKeyboardButton(text="История Ислама", callback_data="cat_type:Islamic History:0")],
    ]
)




admin_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Добавить книгу", callback_data="add_book")],
        [InlineKeyboardButton(text="Создать категорию", callback_data="create_category")],
        [InlineKeyboardButton(text="Добавить админа", callback_data="add_admin")],
        [InlineKeyboardButton(text="Удалить админа", callback_data="delete_admin")],
        [InlineKeyboardButton(text="Удалить категорию", callback_data="delete_category:0")],
        [InlineKeyboardButton(text="⏪Назад", callback_data="back5")],
    ]
)


async def for_question(user_id):
    # for_question = 
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
            text="Ответить на вопрос", 
            callback_data=f"question_answer:{user_id}"
            )]
        ]
        )