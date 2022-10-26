import datetime
import json

from aiogram import types
from aiogram.types import CallbackQuery
from asgiref.sync import sync_to_async

from bot_app.loader import dp
from clients.models import Client, OrderRequest, Day
from aiogram.dispatcher.filters.builtin import Text
from bot_app.keyboards.inline.order import get_date_keyboard, get_children_amount_keyboard, get_time_keyboard, \
    date_callback_data, time_callback_data, \
    children_amount_callback_data


@sync_to_async
def write_to_db(*args):
    print(args)
    order = OrderRequest(
        start_time=args[0].split("-")[0].strip(),
        end_time=args[0].split("-")[1].strip(),
        date=Day.objects.get(date=args[1]),
        children_amount=args[2],
        client=Client.objects.get(telegram_id=args[3])
    )
    order.save()


@dp.message_handler(Text(equals="Записать ребёнка"))
async def choose_day(message: types.Message):
    keyboard = await get_date_keyboard()
    if keyboard is None:
        await message.answer(
            "К сожалению, на ближайшую неделю нет свободных мест. Вы можете попробовать ещё раз немного позже.")

    else:
        await message.answer("Выберите день, на который хотите записать ребёнка:",
                             reply_markup=keyboard)


@dp.callback_query_handler(date_callback_data.filter())
async def choose_time(call: CallbackQuery, callback_data: dict):
    order_date = callback_data.get("date")
    await call.answer()
    await call.message.edit_text(
        text="Выберите время, на которое хотите записать ребёнка:",
        reply_markup=await get_time_keyboard(order_date)
    )


@dp.callback_query_handler(time_callback_data.filter())
async def make_order(call: CallbackQuery, callback_data: dict):
    order_time = callback_data.get("time")
    order_date = callback_data.get("date")
    await call.answer()
    await call.message.edit_text(
        text="Выберите количество детей, которых хотите записать:",
        reply_markup=await get_children_amount_keyboard(order_date, order_time)
    )


@dp.callback_query_handler(children_amount_callback_data.filter())
async def choose_children_amount(call: CallbackQuery, callback_data: dict):
    order_time = callback_data.get("time")
    order_date = callback_data.get("date")
    children_amount = callback_data.get("children_amount")
    client = call.from_user["id"]
    await write_to_db(order_time, order_date, children_amount, client)
