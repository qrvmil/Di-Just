import asyncio
import sqlite3
from datetime import datetime

from aiogram import Bot
from aiogram.enums import ParseMode

from config import TOKEN, FRONT_URL


conn = sqlite3.connect("reminders.db")
cur = conn.cursor()

bot = Bot(token=TOKEN)


async def check():
    while True:
        cur.execute("SELECT * FROM reminders;")
        reminders_results = cur.fetchall()
        time = datetime.now().strftime("%d:%H:%M")
        for x in reminders_results:
            if x[2] == time:
                cur.execute("DELETE FROM reminders WHERE id=%s;" % str(x[0]))
                conn.commit()
                digest_type, digest_id = x[3].split('_')
                type = "img-digest" if digest_type == "img" else "link-digest"
                
                reminder = f"Самое время прочесть дайджест\n" + f"[тык]({FRONT_URL}{type}/{digest_id}/)"
                await bot.send_message(chat_id=x[1], text=reminder, parse_mode=ParseMode.MARKDOWN_V2)

        await asyncio.sleep(60)

async def start():
    current_sec = int(datetime.now().strftime("%S"))
    delay = 60 - current_sec
    if delay == 60:
        delay = 0

    await asyncio.sleep(delay)
    await check()