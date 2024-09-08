import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher,types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart,Command
from aiogram import F
from aiogram.types import Message
from data import config
from filters.admin import IsBotAdminFilter 
from create import sqlite3
from keyboard_button import course_button
from states import Form
from aiogram.fsm.context import FSMContext

ADMINS = config.ADMINS
TOKEN = config.BOT_TOKEN

dp = Dispatcher()
# bot = Bot(TOKEN, parse_mode=ParseMode.HTML)

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    print(message.from_user.id) in ADMINS

    await message.answer(text="Assalomu alaykum")

@dp.message(F.text,IsBotAdminFilter(ADMINS))
async def user_funksiyasi(message:Message):
    await message.answer("Tabriklaymiz siz adminsiz⭐️")

@dp.message(F.text)
async def admin_funksiyasi(message:Message):
    await message.answer("Afsuski siz admin emassiz😔")


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    if str(message.from_user.id) in ADMINS:
        await message.answer(text="Assalomu alaykum",reply_markup=course_button)
    else:
        await message.answer(text="Assalomu alaykum")




@dp.message(CommandStart())
async def command_start_handler(message: Message,state:FSMContext) -> None:
    await state.set_state(Form.first_name)
    full_name = message.from_user.full_name
    connection  = sqlite3.connect("aqulite.db")
    cursor = connection.cursor()
    command = """SELECT telegram_id FROM USERS"""
    cursor.execute(command)
    users_id = cursor.fetchall()
    try:
        users_id = [i[0] for i in users_id]
    except:
        pass
    if message.from_user.id in users_id:
        await message.reply(text="Botimizdan foydalanishingiz mumkin")

    await state.set_state(Form.first_name)    


@dp.message(CommandStart())
async def command_start_handler(message: Message,state:FSMContext) -> None:
    full_name = message.from_user.full_name
    text = f"Assalomu alaykum,{full_name} Sifat botiga hush kelibsiz\nRo'yhatdan o'tish uchun ismingizni kiriting!"
    await message.answer(text=text,reply_markup=course_button)    

 

    text = f"Assalomu alaykum,{full_name} Sifat botiga hush kelibsiz\nRo'yhatdan o'tish uchun ismingizni kiriting!"
    await message.reply(text=text)





@dp.message(F.text=="Foydalanuvchilar soni",IsBotAdminFilter(ADMINS))
async def foydalanuvchilar_soni_menu(message:Message,state:FSMContext):
    connection  = sqlite3.connect("aqulite.db")
    cursor = connection.cursor()
    command = """SELECT count(*) FROM USERS"""
    cursor.execute(command)
    count = cursor.fetchone()
    await message.answer(text=f"Bizning botimizda {count}ta foydalanuvchi bor!")
  

@dp.message(F.text=="Foydalanuvchilar haqida ma'lumot",IsBotAdminFilter(ADMINS))
async def foydalanuvchilar_haqida_malumot_menu(message:Message,state:FSMContext):
    connection  = sqlite3.connect("aqulite.db")
    cursor = connection.cursor()
    command = """SELECT first_name, last_name, phone_number FROM USERS"""
    cursor.execute(command)
    users = cursor.fetchall()
    text = "Bizning foydalanuvchilar:"
    for index,data in enumerate(users):
        text += f"\n{index+1}. Ismi:  {data[0]}\n{index+1}. Familiyasi:  {data[1]}\n{index+1}. Tel:  {data[2]}"   

    await message.answer(text=text)



#bot ishga tushganini xabarini yuborish

async def on_startup_notify(bot: Bot):
    for admin in ADMINS:
        try:
            await bot.send_message(chat_id=int(admin),text="Bot ishga tushdi")
        except Exception as err:
            logging.exception(err)

async def off_startup_notify(bot: Bot):
    for admin in ADMINS:
        try:
            await bot.send_message(chat_id=int(admin),text="Ish tugadi")
        except Exception as err:
            logging.exception(err)

async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await on_startup_notify(bot)
    await dp.start_polling(bot)
    await off_startup_notify(bot)
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
