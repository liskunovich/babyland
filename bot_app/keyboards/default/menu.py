from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

MAIN_MENU_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Записать ребёнка")
        ],
        [
            KeyboardButton(text="Посмотреть активные записи")
        ],
        [
            KeyboardButton(text="Контакты нашего центра")
        ]
    ], resize_keyboard=True
)
