import asyncio

from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.types import message

from bot_app.keyboards.default import menu
from asgiref.sync import sync_to_async
from aiogram.utils.markdown import hbold, hlink, hitalic
from bot_app.loader import dp


@dp.message_handler(Text(equals=[
    'Контакты нашего центра'
]))
async def bot_contacts(message: types.Message):
    await message.answer(f"Наш ('телефон'): +77055553535" + '\n',)
