import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher,types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart,Command
from aiogram import F
from aiogram.types import Message
from wikipediya import wikipedia

TOKEN = "6690273634:AAHArUeXT91Lym5bprRpLOuaN28O7FQL9aI"
dp = Dispatcher()

@dp.message(Command(commands="help"))
async def command_help_handler(message: Message) -> None:
    
    text = "Bot commands\n /start-run the bot\n"
    await message.reply(text)

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    full_name = message.from_user.full_name
    text = f"salom, {full_name}\n bu bot sizga viloyatlar haqida malumot chiqarib beradi  ... !"

    await message.reply(text=text)

@dp.message()
async def sendWikki(message: types.Message):
    try:
        respond = wikipedia.summary(message.text)
        await message.answer(respond)
    except:
        await message.answer("Bu mavzuga oid maqola topilmadi")

async def main() -> None:

    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
