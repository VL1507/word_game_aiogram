from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove


b1 = KeyboardButton("/help")
b2 = KeyboardButton("/countries")
b3 = KeyboardButton("/russian_cities")

buttons = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

# buttons.add(b1).add(b2).add(b3)

buttons.insert(b1).insert(b2).insert(b3)
