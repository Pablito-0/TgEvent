from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from app import TIERS


class SetTier(StatesGroup):
    user = State()
    tier = State()

async def get_one_user(message: types.Message, state: FSMContext):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for tier in TIERS:


