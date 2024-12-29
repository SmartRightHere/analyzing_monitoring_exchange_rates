from aiogram import Dispatcher
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from database import Database

db = Database()


# Состояния для FSM
class IncomeState(StatesGroup):
    waiting_for_income = State()
    waiting_for_expense = State()


def generate_inline_buttons():
    buttons = [
        InlineKeyboardButton(text='Добавить доход', callback_data='add_income'),
        InlineKeyboardButton(text='Добавить расход', callback_data='add_expense'),
        InlineKeyboardButton(text='Посмотреть баланс', callback_data='total'),
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=[buttons])
    return keyboard


# Обработчик для inline кнопок
async def process_callback(callback_query: CallbackQuery, state: FSMContext):
    data = callback_query.data

    if data == 'total':
        user_id = callback_query.from_user.id
        total = db.get_total(user_id)
        await callback_query.message.answer(f'Ваш текущий баланс: {total} рублей')

    elif data == 'add_income':
        await callback_query.message.answer('Введите сумму дохода:')
        await state.set_state(IncomeState.waiting_for_income)

    elif data == 'add_expense':
        await callback_query.message.answer('Введите сумму расхода:')
        await state.set_state(IncomeState.waiting_for_expense)


# Обработка ввода суммы дохода
async def process_income(message: Message, state: FSMContext):
    try:
        amount = float(message.text)
        db.add_income(user_id=message.from_user.id, amount=amount)
        await message.answer(f'Доход в размере {amount} добавлен!')
        await state.clear()
    except ValueError:
        await message.answer('Пожалуйста, введите корректное число.')


# Обработка ввода суммы расхода
async def process_expense(message: Message, state: FSMContext):
    try:
        amount = float(message.text)
        db.add_expense(user_id=message.from_user.id, amount=amount)
        await message.answer(f'Расход в размере {amount} добавлен!')
        await state.clear()
    except ValueError:
        await message.answer('Пожалуйста, введите корректное число.')


# Регистрация обработчиков inline кнопок и FSM
def register_inline_handlers(dp: Dispatcher):
    dp.callback_query.register(process_callback)
    dp.message.register(process_income, IncomeState.waiting_for_income)
    dp.message.register(process_expense, IncomeState.waiting_for_expense)
