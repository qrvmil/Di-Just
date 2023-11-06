from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_date_picker_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Через минуту")
    kb.button(text="В течение часа")
    kb.button(text="Утром")
    kb.button(text="Вечером")
    kb.button(text="Завтра")
    kb.button(text="Через неделю")
    kb.adjust(3)
    return kb.as_markup(resize_keyboard=True)


available_date_picker = ["Через минуту", "В течение часа", "Утром", "Вечером", "Завтра", "Через неделю"]
