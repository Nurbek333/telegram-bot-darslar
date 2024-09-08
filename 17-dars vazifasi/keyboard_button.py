from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton,ReplyKeyboardMarkup,KeyboardButton

inline_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Menu",callback_data='course')],

    ]
)
course_button = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Foydalanuvchilar soni"),
        KeyboardButton(text="Foydalanuvchilar haqida ma'lumot")],
    ],
    resize_keyboard=True,
    input_field_placeholder="Tugmalardan birini tanlang"
)
