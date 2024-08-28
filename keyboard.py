from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

# Qo'shimcha tugmalar va tasvirlar bilan keyboard
keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🌍 Davlat Valyutalari kursi"), KeyboardButton(text="Kripto yangiliklari")],
        [KeyboardButton(text="💎 Kriptovalyutalar kursi"), KeyboardButton(text="📈 Valyuta nima")],
        [KeyboardButton(text="📊 Bot statistikasi"), KeyboardButton(text="Tarixiy narx")],
    ],
    resize_keyboard=True,
)


keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🌍 Davlat Valyutalari kursi"), KeyboardButton(text="💎 Kriptovalyutalar kursi")],
        [KeyboardButton(text="📊 Bot statistikasini ko'rsatish")],
    ],
    resize_keyboard=True,
)
