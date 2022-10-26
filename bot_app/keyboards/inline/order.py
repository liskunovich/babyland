from datetime import timedelta, datetime

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from asgiref.sync import sync_to_async
from django.db import models
from django.utils import timezone

from clients.models import Day

date_callback_data = CallbackData('order', 'action', 'date')
time_callback_data = CallbackData('order', 'action', 'date', 'time', sep='!')
children_amount_callback_data = CallbackData('order', 'action', 'date', 'time', 'children_amount', sep='!')


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
                                        callback_data=date_callback_data.new(
                                            action='choose_day',
                                            date=day['date']
                                        ))
                   for day in week]
        for i in range(0, len(week)):
            keyboard.insert(buttons[i])
        return keyboard


@sync_to_async
def get_time_keyboard(date):
    start_time_list = ["9:00", "9:30", "10:00", "10:30", "11:00", "11:30", "12:00", "12:30", "13:00", "13:30"]
    end_time_list = ["13:00", "13:30", "14:00", "14:30", "15:00", "15:30", "16:00", "16:30", "17:00", "17:30"]
    keyboard = InlineKeyboardMarkup(row_width=3)
    buttons = [
        InlineKeyboardButton(
            text=f"{x} - {y}",
            callback_data=time_callback_data.new(
                action='choose_time',
                date=date,
                time=f'{x}-{y}',
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
        callback_data=children_amount_callback_data.new(
            action='choose_children',
            date=date,
            time=time,
            children_amount=i + 1
        )
    ) for i in range(0, 10)]
    for i in range(len(buttons)):
        keyboard.insert(buttons[i])
    return keyboard
