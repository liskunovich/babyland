from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from bot_app.keyboards.default import start, menu
from clients.models import Client
from asgiref.sync import sync_to_async
from loader import dp


@sync_to_async
def write_to_db(*args):
    cl = Client(telegram_id=args[0], username=args[1], number=args[2])
    cl.save()


@sync_to_async
def is_exists(telegram_id: str):
    return Client.objects.filter(telegram_id=telegram_id).exists()


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f'Привет, {message.from_user.full_name}!',
                         reply_markup=start.PHONE_REQUEST_KEYBOARD if not (
                             await is_exists(message.from_user.id)) else menu.MAIN_MENU_KEYBOARD)
    user_id = message.from_user.id
    username = message.from_user.username
    await write_to_db(user_id, username, None)


@dp.message_handler(content_types=types.ContentType.CONTACT)
async def get_number(message: types.Contact):
    message_data = message.contact
    if await is_exists(message_data["user_id"]):
        await message.answer("Вы перешли в главное меню", reply_markup=menu.MAIN_MENU_KEYBOARD)
    else:
        await write_to_db(message_data["user_id"], message_data["first_name"], message_data["phone_number"])
