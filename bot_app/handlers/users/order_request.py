import datetime

from aiogram import types
from asgiref.sync import sync_to_async

from bot_app.loader import dp
from clients.models import Client, OrderRequest
from aiogram.dispatcher.filters.builtin import Text
from bot_app.keyboards.inline.order import get_order_keyboard


@sync_to_async
def write_to_db(*args):
    ...


@dp.message_handler(Text(equals="Записать ребёнка"))
async def make_order(message: types.Message):
    await message.answer("Выберите день, на который хотите записать ребёнка:", reply_markup=await get_order_keyboard())
