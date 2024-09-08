import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher,types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart,Command
from aiogram import F
from aiogram.types import Message,CallbackQuery
from aiogram.fsm.context import FSMContext
from states import Form
from create import sqlite3
from keyboard_button import course_button


#regular expression uchun
import re # yangi qo'shildi e'tibor bering


ADMIN = 6214256605 # Bu yerga id kiriting
TOKEN = "6690273634:AAHArUeXT91Lym5bprRpLOuaN28O7FQL9aI" #Token kiriting
dp = Dispatcher()
bot = Bot(TOKEN, parse_mode=ParseMode.HTML)


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
        await message.reply(text="Botimizdan foydalanishingiz mumkin",reply_markup=course_button)

    await state.set_state(Form.first_name)    


@dp.message(CommandStart())
async def command_start_handler(message: Message,state:FSMContext) -> None:
    full_name = message.from_user.full_name
    text = f"Assalomu alaykum,{full_name} Sifat botiga hush kelibsiz\nRo'yhatdan o'tish uchun ismingizni kiriting!"
    await message.answer(text=text,reply_markup=course_button)    
    

    text = f"Assalomu alaykum,{full_name} Sifat botiga hush kelibsiz\nRo'yhatdan o'tish uchun ismingizni kiriting!"
    await message.reply(text=text)

    

@dp.message(F.text=="Foydalanuvchilar soni")
async def foydalanuvchilar_soni_menu(message:Message,state:FSMContext):
    connection  = sqlite3.connect("aqulite.db")
    cursor = connection.cursor()
    command = """SELECT count(*) FROM USERS"""
    cursor.execute(command)
    count = cursor.fetchone()
    await message.answer(text=f"Bizning botimizda {count}ta foydalanuvchi bor!")

@dp.message(F.text=="Foydalanuvchilar haqida ma'lumot")
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


@dp.message(Form.first_name,F.text)
async def get_first_name(message:Message,state:FSMContext):

    first_name = message.text
    await state.update_data(first_name=first_name)

    await state.set_state(Form.last_name)
    text = f"Familyangizni kiriting!"
    await message.reply(text=text)

@dp.message(Form.last_name, F.text)
async def get_last_name(message:Message,state:FSMContext):

    last_name = message.text
    await state.update_data(last_name=last_name)

    await state.set_state(Form.photo)
    text = f"Rasmingizni yuboring!"
    await message.reply(text=text)


#rasm uchun dispacher handler state 
@dp.message(Form.photo,F.photo)
async def get_photo(message:Message,state:FSMContext):

    photo = message.photo[-1].file_id #rasmni file id sini saqlab olamiz
    await state.update_data(photo=photo)
    await state.set_state(Form.phone_number)
    text = f"Telefon nomeringizni kiriting!"
    await message.reply(text=text)

#rasmdan boshqa narsa yuborilsa javob qaytaramiz
@dp.message(Form.photo)
async def not_get_photo(message:Message,state:FSMContext):
    text = f"Iltimos rasm yuboring!"
    await message.reply(text=text)



#telefon nomer uchun
@dp.message(Form.phone_number)
async def get_phone_number(message:Message,state:FSMContext):
    pattern = "^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$"
    #shart beramiz
    #telefon nomer to'g'ri kiritilgan bo'lsa ishlaydi
    if re.match(pattern,message.text):

        phone_number = message.text
        await state.update_data(phone_number=phone_number)

        await state.set_state(Form.age)
        text = f"Yoshingizni kiriting!"
        await message.reply(text=text)
    #aks holda esa telefon nomerni to'g'ri kiritishini so'raymiz.
    else:
        await message.reply(text="telefon nomeringizni noto'g'ri kiritdingiz")



@dp.message(Form.age,F.text)
async def age_get(message:Message,state:FSMContext):
    age = message.text
    if age.isdigit():
        await state.update_data(age=age)

        await state.set_state(Form.sinf)
        text = f"Sinfingizni kiriting!"
        await message.reply(text=text)
    else:
        await message.reply("Noto'g'ri")

@dp.message(Form.age)
async def not_age(message:Message,state:FSMContext):
    await message.reply("Text ko'rinishida ma'lumot kiriting")


@dp.message(Form.sinf,F.text)
async def sinf_get(message:Message,state:FSMContext):
    sinf = message.text
    if sinf.isdigit():
        await state.update_data(sinf=sinf)

        await state.set_state(Form.hobby)
        text = f"Hobbyingizni kiriting!"
        await message.reply(text=text)
    else:
        await message.reply("Noto'g'ri")

@dp.message(Form.sinf)
async def not_sinf(message:Message,state:FSMContext):
    await message.reply("Text ko'rinishida ma'lumot kiriting")


@dp.message(Form.hobby,F.text)
async def hobby_get(message:Message,state:FSMContext):
    hobby = message.text
    if hobby.isalpha():
        await state.update_data(hobby=hobby)

        await state.set_state(Form.fruit)
        text = f"Yaxshi ko'rgan mevangizni kiriting!"
        await message.reply(text=text)
    else:
        await message.reply("Noto'g'ri")

@dp.message(Form.hobby)
async def not_hobby(message:Message,state:FSMContext):
    await message.reply("Text ko'rinishida ma'lumot kiriting")
 

@dp.message(Form.fruit,F.text)
async def fruit_get(message:Message,state:FSMContext):
    fruit = message.text
    if fruit.isalpha():
        await state.update_data(fruit=fruit)

        await state.set_state(Form.home_number)
        text = f"Uyingiz raqamini kiriting!"
        await message.reply(text=text)
    else:
        await message.reply("Noto'g'ri")

@dp.message(Form.fruit)
async def not_fruit(message:Message,state:FSMContext):
    await message.reply("Text ko'rinishida ma'lumot kiriting")



@dp.message(Form.home_number,F.text)
async def home_number_get(message:Message,state:FSMContext):
    number = message.text
    if number.isdigit():
        await state.update_data(home_number=number)

        await state.set_state(Form.address)
        text = f"Manzilingizni kiriting!"
        await message.reply(text=text)
    else:
        await message.reply("Noto'g'ri")

@dp.message(Form.home_number)
async def not_hom_number(message:Message,state:FSMContext):
    await message.reply("Text ko'rinishida ma'lumot kiriting")



@dp.message(Form.address)
async def get_address(message:Message,state:FSMContext):

    address = message.text
    await state.update_data(address=address)

    data = await state.get_data()
    
    my_photo = data.get("photo") #rasmni qabul qilib olish
    first_name = data.get("first_name")
    last_name = data.get("last_name")                   
    phone_number = data.get("phone_number")
    address = data.get("address")
    telegram_id = message.from_user.id
    home_number = data.get("home_number")
    age = data.get("age")
    sinf = data.get("sinf")
    hobby = data.get("hobby")
    fruit = data.get("fruit")



    try:
        connection  = sqlite3.connect("aqulite.db")
        cursor = connection.cursor()
        command = f"""
            INSERT INTO USERS('first_name','last_name','phone_number','telegram_id','address','home_number','age','sinf','hobby','fruit')
            VALUES('{first_name}','{last_name}','{phone_number}','{telegram_id}','{address}','{home_number}','{age}','{sinf}','{hobby}','{fruit}');
        """
        cursor.execute(command)
        connection.commit()

    except:
        pass   
    text = f"<b>Ariza</b>\nIsmi:  {first_name}\nFamilyasi:  {last_name}\nTel:  {phone_number}\nManzil:  {address}\nUy raqami:  {home_number}\nYoshi:  {age}\nSinfi:  {sinf}\nHobbyi:  {hobby}\nYaxshi ko'rgan mevasi:  {fruit}"
    
    #adminga ariza ma'lumotlarini yuboramiz

    await bot.send_photo(ADMIN,photo=my_photo,caption=text)
    # print(first_name,last_name,phone_number,address)
    

    await state.clear()
    text = f"Siz muvaffaqiyatli tarzda ro'yhatdan o'tdingiz🎉"
    await message.reply(text=text, reply_markup=course_button)


async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
