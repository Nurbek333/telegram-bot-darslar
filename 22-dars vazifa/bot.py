from aiogram import Bot, Dispatcher,types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart,Command
from aiogram import F
from aiogram.types import Message
from data import config
import asyncio
import logging
import sys
from baza.create import users_db
from baza.add_user import add as add_user
from filters.admin import IsBotAdminFilter
from keyboard_buttons import admin_keyboard
from baza.all_users import allusers,allusers_id
from aiogram.fsm.context import FSMContext #new
from states.reklama import Adverts
import time 
from remove_bg import removebg
from filters.check_sub_channel import IsCheckSubChannels
from filters.admin import IsBotAdminFilter
ADMINS = config.ADMINS
TOKEN = config.BOT_TOKEN
CHANNELS = config.CHANNELS

dp = Dispatcher()
bot = Bot(TOKEN, parse_mode=ParseMode.HTML)

# forward qilingan xabarlar chat id sini oladi
# @dp.message(F.forward_from_chat)
# async def check_channel_id(message:Message):
#     await message.answer(f"CHannel id: {message.forward_from_chat.id}")

# @dp.message(IsCheckSubChannels())
# async def is_check_sub_channel(message:Message):
#     await message.answer(text="Botdan foydalanishingiz mumkin")

# @dp.message(IsCheckSubChannels())
# async def kanalga_obuna(message:Message):
#     text = ""
#     for index,channel in enumerate(CHANNELS):
#         ChatInviteLink = await bot.create_chat_invite_link(CHANNELS[0])
#         text += f"{indeex}- {ChatInviteLink}\n"
#         await message.answer(f"{ChatInviteLink.invite_link}>1-kanalkanaliga azo bo'ling")


@dp.message(CommandStart())
async def start_command(message:Message):
    full_name = message.from_user.full_name
    telegram_id = message.from_user.id
    try:
        add_user(full_name=full_name,telegram_id=telegram_id)
        text = f"Assalomu alaykum,{full_name}\nBu bot rasm orqa fonini o'chirib beradi. Botdan foydalanish uchun rasm yuboring!!!"

        await message.answer(text=text)
    except:
        await message.answer(text="Assalomu alaykum")


@dp.message(Command("admin"),IsBotAdminFilter(ADMINS))
async def is_admin(message:Message):
    await message.answer(text="Admin menu",reply_markup=admin_keyboard.admin_button)


@dp.message(F.text=="Foydalanuvchilar soni",IsBotAdminFilter(ADMINS))
async def users_count(message:Message):
    counts = allusers()
    text = f"Botimizda {counts[0]} ta foydalanuvchi bor"
    await message.answer(text=text)

@dp.message(F.text=="Reklama yuborish",IsBotAdminFilter(ADMINS))
async def advert_dp(message:Message,state:FSMContext):
    await state.set_state(Adverts.adverts)
    await message.answer(text="Reklama yuborishingiz mumkin !")




@dp.message(Adverts.adverts)
async def send_advert(message:Message,state:FSMContext):
    message_id = message.message_id
    from_chat_id = message.from_user.id
    users = allusers_id()
    count = 0
    for user in users:
        try:
            await bot.copy_message(chat_id=user[0],from_chat_id=from_chat_id,message_id=message_id)
            time.sleep(1)
            count += 1
        except:
            pass
        time.sleep(0.5)
    
    await message.answer(f"Reklama {count}ta foydalanuvchiga yuborildi")
    await state.clear()


@dp.message(F.photo)
async def name(message:Message):
    file_id = message.photo[-1].file_id
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    file = await bot.get_file(file_id)
    file_path = file.file_path
    photos_url = f"https://api.telegram.org/file/bot{TOKEN}/{file_path}"
    rasm = removebg(photos_url)
    if rasm:
        await message.answer_photo(photo=types.input_file.BufferedInputFile(rasm,filename="no-remove.png"))
        await message.answer_document(document=types.input_file.BufferedInputFile(rasm,filename="no-remove.png"))



@dp.message()
async def text_message(message:Message):
    message.answer("Iltimos, rasm yuboring!!!")


@dp.startup()
async def on_startup_notify(bot: Bot):
    for admin in ADMINS:
        try:
            await bot.send_message(chat_id=int(admin),text="Bot ishga tushdi")
        except Exception as err:
            logging.exception(err)

#bot ishga tushganini xabarini yuborish
@dp.shutdown()
async def off_startup_notify(bot: Bot):
    for admin in ADMINS:
        try:
            await bot.send_message(chat_id=int(admin),text="Bot ishdan to'xtadi!")
        except Exception as err:
            logging.exception(err)



async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    users_db() #database yaratildi
    dp.message.register(kanalga_obuna,IsCheckSubChannels())
    await dp.start_polling(bot)




if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
