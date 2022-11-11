from datetime import timedelta, datetime

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from asgiref.sync import sync_to_async
from django.db import models
from django.utils import timezone

from clients.models import Day

order_callback_data = CallbackData('order', 'action', 'date', 'time', 'children_amount', sep='!')


@sync_to_async
def get_date_keyboard():
    now = timezone.now()
    week = Day.objects.filter(is_available=True, date__gte=now, date__lte=now + timedelta(days=6)).values()
    if len(week) == 0:
        return None
    else:
        keyboard = InlineKeyboardMarkup(row_width=2)
        buttons = [InlineKeyboardButton(text=
                                        f"{day['week_day']}({day['date'].strftime('%Y-%m-%d')})",
                                        callback_data=order_callback_data.new(
                                            action='set_date',
                                            date=day['date'],
                                            time=' ',
                                            children_amount=' '
                                        ))
                   for day in week]
        for i in range(0, len(week)):
            keyboard.insert(buttons[i])
        return keyboard


@sync_to_async
def get_time_keyboard(date):
    day = Day.objects.get(date=date)
    start_time_list = ["9:00", "9:30", "10:00", "10:30", "11:00", "11:30", "12:00", "12:30", "13:00", "13:30"]
    end_time_list = ["13:00", "13:30", "14:00", "14:30", "15:00", "15:30", "16:00", "16:30", "17:00", "17:30"]
    if day.week_day == 'Суббота':
        start_time_list = start_time_list.copy()[:len(start_time_list) - 3]
        end_time_list = end_time_list.copy()[:len(end_time_list) - 3]
    keyboard = InlineKeyboardMarkup(row_width=3)
    buttons = [
        InlineKeyboardButton(
            text=f"{x} - {y}",
            callback_data=order_callback_data.new(
                action='set_time',
                date=date,
                time=f'{x}-{y}',
                children_amount=' '
            )
        ) for x, y in zip(start_time_list, end_time_list)
    ]
    for i in range(len(buttons)):
        keyboard.insert(buttons[i])
    return keyboard


@sync_to_async
def get_children_amount_keyboard(date, time):
    keyboard = InlineKeyboardMarkup(row_width=3)
    buttons = [InlineKeyboardButton(
        text=str(i + 1),
        callback_data=order_callback_data.new(
            action='set_children',
            date=date,
            time=time,
            children_amount=i + 1
        )
    ) for i in range(0, 10)]
    for i in range(len(buttons)):
        keyboard.insert(buttons[i])
    return keyboard


@sync_to_async
def get_cancel_keyboard(date, time, children_amount):
    keyboard = InlineKeyboardMarkup(row_width=1)
    button = InlineKeyboardButton(
                text="Отменить запись",
                callback_data=order_callback_data.new(
                    action='cancel_order',
                    date=date,
                    time=time,
                    children_amount=children_amount
                )
            )
    keyboard.insert(button)
    return keyboard

