from aiogram import F, Bot, types, Router
from aiogram.types import CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

from FSM.fsm import QuestionAnswer
from filters.chat_types import ChatTypeFilter
from keyboards import reply


chat_router = Router()
chat_router.message.filter(ChatTypeFilter(['group', 'supergroup']))

# @chat_router.message()
# async def hello_command(message: types.Message):
#     await message.answer(str(message.chat.id))
#     await message.answer(f"Ваш ID: {message.from_user.id}")
#     await message.answer(f'@{message.from_user.username}')

#     await message.answer("Приветствую вас в чате!")

@chat_router.callback_query(F.data.startswith("question_answer:"))
async def question_answer(callback: CallbackQuery, state: FSMContext):
    user_id = int(callback.data.split(':')[1])
    await state.set_state(QuestionAnswer.answer)
    await state.update_data(user_id=user_id, scientist=callback.from_user.id)
    await callback.message.edit_text(f'@{callback.from_user.username} захотел ответить на данный вопрос, ждём вашего ответа')
    await callback.answer()


@chat_router.message(QuestionAnswer.answer)
async def answer(message: types.Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    if data['scientist'] == message.from_user.id:
        user_id = data['user_id']
        await bot.send_message(chat_id=data['user_id'], text=f'Ответ на ваш вопрос: {message.text}')
        await message.answer(f'@{message.from_user.username}, ваш ответ был доставлен')
        await state.clear()
    else:
        await state.set_state(QuestionAnswer)