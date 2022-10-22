from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from asgiref.sync import sync_to_async

from clients.models import Day


@sync_to_async
def get_order_keyboard():
    week = Day.objects.filter(is_workday=True).values()
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=day['day'], callback_data=day['day']) for day in week]
    ])
    return keyboard
