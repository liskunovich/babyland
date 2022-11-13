from datetime import timedelta, datetime
from typing import List, Dict

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from asgiref.sync import sync_to_async
from django.db import models
from django.utils import timezone

from clients.models import Day

order_callback_data = CallbackData('order', 'action', 'date', 'time', 'children_amount', sep='!')


def order_keyboard_constructor(iterable, kwargs: List[dict], has_back=True):
    keyboard = InlineKeyboardMarkup()
    for i in range(len(iterable)):
        keyboard.insert(
            InlineKeyboardButton(text=iterable[i], callback_data=order_callback_data.new(**kwargs[i]))
        )
    return keyboard


def get_date_keyboard():
    now = timezone.now()
    week = Day.objects.filter(is_available=True, date__gte=now, date__lte=now + timedelta(days=6)).values()
    if len(week) == 0:
        return None
    else:
        buttons = [f"{day['week_day']}({day['date'].strftime('%d-%m-%Y')})" for day in week]
        kwargs = [
            {"action": "set_date",
             "date": day["date"],
             "time": " ",
             "children_amount": " "}
            for day in week
        ]
        return buttons, kwargs


def get_time_keyboard(date):
    day = Day.objects.get(date=date)
    start_time_list = ["9:00", "9:30", "10:00", "10:30", "11:00", "11:30", "12:00", "12:30", "13:00", "13:30"]
    end_time_list = ["13:00", "13:30", "14:00", "14:30", "15:00", "15:30", "16:00", "16:30", "17:00", "17:30"]
    if day.week_day == 'Суббота':
        start_time_list = start_time_list.copy()[:len(start_time_list) - 3]
        end_time_list = end_time_list.copy()[:len(end_time_list) - 3]
    keyboard = InlineKeyboardMarkup(row_width=3)
    buttons = [f"{x} - {y}" for x, y in zip(start_time_list, end_time_list)]
    kwargs = [
        {"action": "set_time",
         "date": day.date,
         "time": button,
         "children_amount": " "}
        for button in buttons
    ]
    return buttons, kwargs


def get_children_amount_keyboard(date, time):
    buttons = [i for i in range(1, 11)]
    kwargs = [
        {"action": "set_children",
         "date": date,
         "time": time,
         "children_amount": i + 1}
        for i in range(len(buttons))
    ]
    return buttons, kwargs

