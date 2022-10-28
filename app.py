import logging
import os

import requests
from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
from aiogram.dispatcher.filters import Text

from event_serv import event_service
from states import SetTier

load_dotenv()

logging.basicConfig(level=logging.INFO)

bot = Bot(token=os.environ["API_TOKEN"])
dp = Dispatcher(bot)
TIERS = ['Gold','Silver','Bronze']

async def startup(_):
    response = requests.get("http://127.0.0.1:8000/admin/event/customuser/")
    response.raise_for_status()


@dp.message_handler(commands=["admin"])
async def get_admin_commands(msg: types.Message):
    inline_kb = types.InlineKeyboardMarkup(row_width=1)
    inline_kb.add(types.InlineKeyboardButton("Get users", callback_data="get_users_1"))
    inline_kb.add(types.InlineKeyboardButton("Add event", callback_data="add_event_1"))
    await msg.reply("Choose admin action", reply_markup=inline_kb)


@dp.callback_query_handler(Text(contains="get_users"))
async def display_users(callback: types.CallbackQuery):
    page = int(callback.data.split("_")[-1])
    users_response = event_service.get_users(page)
    inline_kb = types.InlineKeyboardMarkup(row_width=1)

    for user in users_response["results"]:
        inline_kb.add(
            types.InlineKeyboardButton(f"{user['id']}. {user['username']}", callback_data=f"user_id:{user['id']}")
        )

    pagination_buttons = []
    if users_response['previous']:
        pagination_buttons.append(types.InlineKeyboardButton("Prev", callback_data=f"get_users_{page - 1}"))
    if users_response['next']:
        pagination_buttons.append(types.InlineKeyboardButton("Next", callback_data=f"get_users_{page + 1}"))

    await callback.message.edit_text("Got it", reply_markup=inline_kb.row(*pagination_buttons))


@dp.callback_query_handler(Text(contains="user_id"))
async def display_user(callback: types.CallbackQuery):
    user_id = int(callback.data.split(":")[-1])
    user = event_service.get_user(user_id)

    inline_kb = types.InlineKeyboardMarkup(row_width=1)
    pagination_buttons = []
    inline_kb.add(
        types.InlineKeyboardButton(f"id: {user['id']}, name: {user['username']}, tier: {user['tier']}",
                                   callback_data=f"user_id:{user['id']}")
    )
    inline_kb.add(
        types.InlineKeyboardButton('Change tier',callback_data='change_tier'))

    await callback.message.edit_text("Got it", reply_markup=inline_kb.row(*pagination_buttons))
    await SetTier.user.state()


@dp.callback_query_handler(Text(equals='change_tier'))
async def change_tier(callback: types.CallbackQuery):
    inline_kb = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True, resize_keyboard=True)

    for tier in TIERS:
        inline_kb.add(types.InlineKeyboardButton(tier))

    await callback.message.answer('Choose Tier', reply_markup=inline_kb)


executor.start_polling(dp, skip_updates=True, on_startup=startup)
