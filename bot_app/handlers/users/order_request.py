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
    order_callback_data, get_cancel_keyboard

from django.db.models import Count, Sum, Q


@sync_to_async
def is_free(time: str, date: str):
    start_time = time.split("-")[0].split(":")[0]
    end_time = time.split("-")[1].split(":")[0].split(":")[0]
    print(start_time, end_time)
    print(time)
    orders = OrderRequest.objects.filter(date=Day.objects.get(date=date))
    orders_time = [order.children_amount for order in orders if abs(int(order.start_time.hour) - int(start_time)) < 4]
    if sum(orders_time) >= 10:
        print("No access")
    else:
        print("Yes access")
    print(orders_time)


@sync_to_async
def write_to_db(*args):
    # order, created = OrderRequest.objects.get_or_create(
    #     start_time=args[0].split("-")[0].strip(),
    #     end_time=args[0].split("-")[1].strip(),
    #     date=Day.objects.get(date=args[1]),
    # )
    # if not created:
    #     order.children_amount += int(args[2])
    #     order.save()
    # else:
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
    keyboard = await get_date_keyboard()
    if keyboard is None:
        await message.answer(
            "К сожалению, на ближайшую неделю нет свободных мест. Вы можете попробовать ещё раз немного позже.")

    else:
        await message.answer("Выберите день, на который хотите записать ребёнка:",
                             reply_markup=keyboard)


@dp.callback_query_handler(order_callback_data.filter(action="set_date"))
async def set_date(call: CallbackQuery, callback_data: dict):
    order_date = callback_data.get("date")
    await call.answer()
    await call.message.edit_text(
        text="Выберите время, на которое хотите записать ребёнка:",
        reply_markup=await get_time_keyboard(order_date)
    )


@dp.callback_query_handler(order_callback_data.filter(action="set_time"))
async def set_time(call: CallbackQuery, callback_data: dict):
    order_time = callback_data.get("time")
    order_date = callback_data.get("date")
    await call.answer()
    await call.message.edit_text(
        text="Выберите количество детей, которых хотите записать:",
        reply_markup=await get_children_amount_keyboard(order_date, order_time)
    )


@dp.callback_query_handler(order_callback_data.filter(action="set_children"))
async def set_children_amount(call: CallbackQuery, callback_data: dict):
    order_time = callback_data.get("time")
    order_date = callback_data.get("date")
    children_amount = callback_data.get("children_amount")
    client = call.from_user["id"]
    await is_free(order_time, order_date)
    # await write_to_db(order_time, order_date, children_amount, client)
    await call.answer()
    await call.message.edit_text(
        text=f"Вы успешно записались на {order_time}",
        reply_markup=await get_cancel_keyboard(order_date, order_time, children_amount)
    )


@dp.callback_query_handler(order_callback_data.filter(action="cancel_order"))
async def cancel_order(call: CallbackQuery, callback_data: dict):
    order_date = callback_data.get("date")
    order_time = callback_data.get("time")
    children_amount = callback_data.get("children_amount")
    client = call.from_user["id"]
    await delete_from_db(order_time, order_date, children_amount, client)
    await call.answer()
    await call.message.edit_text(text="*Запись успешно отменена*", reply_markup=None, parse_mode='Markdown')
