import datetime
import json
from time import strftime

from aiogram import types
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from asgiref.sync import sync_to_async

from bot_app.loader import dp
from clients.models import Client, OrderRequest, Day
from aiogram.dispatcher.filters.builtin import Text
from bot_app.keyboards.inline.order import get_date_keyboard, get_children_amount_keyboard, get_time_keyboard, \
    order_callback_data, order_keyboard_constructor

from django.db.models import Count, Sum, Q


@sync_to_async
def is_free(time: str, date: str, children_amount: int):
    start_time = time.split("-")[0].split(":")[0]
    end_time = time.split("-")[1].split(":")[0].split(":")[0]
    children = children_amount
    orders = OrderRequest.objects.filter(date=Day.objects.get(date=date))
    total_children = [order.children_amount for order in orders if
                      abs(int(order.start_time.hour) - int(start_time)) < 4]
    if sum(total_children) + children <= 10:
        return True, 1
    else:
        return False, 10 - sum(total_children)


@sync_to_async
def write_to_db(*args):
    order = OrderRequest(
        start_time=args[0].split("-")[0].strip(),
        end_time=args[0].split("-")[1].strip(),
        date=Day.objects.get(date=args[1]),
        children_amount=args[2],
        client=Client.objects.get(telegram_id=args[3])
    )
    order.save()


@sync_to_async
def delete_from_db(*args):
    order = OrderRequest.objects.filter(
        start_time=args[0].split("-")[0].strip(),
        end_time=args[0].split("-")[1].strip(),
        date=Day.objects.get(date=args[1]),
        children_amount=args[2],
        client=Client.objects.get(telegram_id=args[3])
    ).delete()
    return True


@dp.message_handler(Text(equals="Записать ребёнка"))
async def set_day(message: types.Message):
    buttons, kwargs = get_date_keyboard()
    keyboard = order_keyboard_constructor(buttons, kwargs)
    if keyboard is None:
        await message.answer(
            "К сожалению, на ближайшую неделю нет свободных мест. Вы можете попробовать ещё раз немного позже.")

    else:
        await message.answer("Выберите день, на который хотите записать ребёнка:",
                             reply_markup=keyboard)


@dp.callback_query_handler(order_callback_data.filter(action="set_date"))
async def set_date(call: CallbackQuery, callback_data: dict):
    order_date = callback_data.get("date")
    buttons, kwargs = get_time_keyboard(order_date)
    keyboard = order_keyboard_constructor(buttons, kwargs)
    await call.answer()
    await call.message.edit_text(
        text="Выберите время, на которое хотите записать ребёнка:",
        reply_markup=keyboard
    )


@dp.callback_query_handler(order_callback_data.filter(action="set_time"))
async def set_time(call: CallbackQuery, callback_data: dict):
    order_time = callback_data.get("time")
    order_date = callback_data.get("date")
    buttons, kwargs = get_children_amount_keyboard(order_date, order_time)
    keyboard = order_keyboard_constructor(buttons, kwargs)
    await call.answer()
    await call.message.edit_text(
        text="Выберите количество детей, которых хотите записать:",
        reply_markup=keyboard
    )


@dp.callback_query_handler(order_callback_data.filter(action="set_children"))
async def set_children_amount(call: CallbackQuery, callback_data: dict):
    order_time = callback_data.get("time")
    order_date = callback_data.get("date")
    children_amount = int(callback_data.get("children_amount"))
    client = call.from_user["id"]
    access, value = await is_free(order_time, order_date, children_amount)
    if access:
        await write_to_db(order_time, order_date, children_amount, client)
        await call.message.edit_text(
            text=f"*Вы успешно записались на {order_time}*", parse_mode='Markdown',
        )
    else:
        sentence = "ребёнка" if value == 1 else "детей"
        await call.message.edit_text(
            text=f"*К сожалению, на это время нет свободных мест*" + '\n' +
                 f"Вы можете записать только *{value}* {sentence}", parse_mode='Markdown',
        )
    await call.answer()


@dp.callback_query_handler(order_callback_data.filter(action="cancel_order"))
async def cancel_order(call: CallbackQuery, callback_data: dict):
    order_date = callback_data.get("date")
    order_time = callback_data.get("time")
    children_amount = callback_data.get("children_amount")
    client = call.from_user["id"]
    await delete_from_db(order_time, order_date, children_amount, client)
    await call.answer()
    await call.message.edit_text(text="*Запись успешно отменена*", reply_markup=None, parse_mode='Markdown')


@dp.callback_query_handler(order_callback_data.filter(action="back"))
async def get_back(call: CallbackQuery, callback_data: dict):
    keyboard_to_back = callback_data.get("")
    print(callback_data)
    await call.answer()
    await call.message.edit_text(text='123')
