import asyncio
import logging
import sqlite3
import datetime
import time

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram import F
from aiogram.types import ReplyKeyboardRemove

from config import TOKEN, FRONT_URL
from keyboard import get_date_picker_kb, available_date_picker
from reminders import start as reminders_run

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token=TOKEN)
# Диспетчер
dp = Dispatcher()
conn = sqlite3.connect("reminders.db")


class ReminderMaker(StatesGroup):
    waiting_for_date = State()


# Хэндлер на команду /start
@dp.message(StateFilter(None), Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    start_command, *args = message.text.split()
    await state.update_data(dijest_id=args[0])
    await message.answer(f"Когда тебе напомнить о дайджесте?", reply_markup=get_date_picker_kb())
    print(args)
    await state.set_state(ReminderMaker.waiting_for_date)


@dp.message(ReminderMaker.waiting_for_date, F.text.in_(available_date_picker))
async def food_size_chosen(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    await message.answer(
        text=f"✨Я напомню про этот дайджест {message.text.lower()}✨",
        reply_markup=ReplyKeyboardRemove()
    )
    date = message.text.lower()
    await state.clear()
    if date == "через минуту":
        delta = datetime.timedelta(minutes=1)
    if date == "в течение часа":
        delta = datetime.timedelta(hours=1)
    if date == "утром":
        if datetime.datetime.now().hour > 9:
            delta = datetime.timedelta(hours=24 - datetime.datetime.now().hour + 9)
        else:
            delta = datetime.timedelta(hours=9 - datetime.datetime.now().hour)
    if date == "вечером":
        if datetime.datetime.now().hour > 18:
            delta = datetime.timedelta(hours=24 - datetime.datetime.now().hour + 18)
        else:
            delta = datetime.timedelta(hours=18 - datetime.datetime.now().hour)
    if date == "завтра":
        delta = datetime.timedelta(days=1)
    if date == "через неделю":
        delta = datetime.timedelta(days=7)

    time = (datetime.datetime.now() + delta).strftime("%d:%H:%M")
    cur = conn.cursor()
    cur.execute("INSERT INTO reminders (user_chat_id, time, info) VALUES (%s, '%s', '%s');" % (
    message.from_user.id, time, user_data['dijest_id']))
    conn.commit()


# Запуск процесса поллинга новых апдейтов
async def main():
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS "reminders" (
    "id"	INTEGER,
    "user_chat_id"	INTEGER,
    "time"	TEXT,
    "info"	TEXT,
    PRIMARY KEY("id")
    )''')
    conn.commit()
    asyncio.ensure_future(reminders_run())
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
