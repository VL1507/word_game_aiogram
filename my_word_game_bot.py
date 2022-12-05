import sqlite3
from random import choice
from aiogram import Bot, Dispatcher, types, executor

from keyboards import buttons
from database import create_db, insert_update_table, game
from word_lists import list_of_countries, list_of_russian_cities


"""     @my_word_game_bot     """


bot = Bot(token='', parse_mode="HTML")
dp = Dispatcher(bot=bot)


@dp.message_handler(commands=["start", "help"])
async def start_help(msg: types.Message):
    insert_update_table(msg.from_user.id, msg.from_user.username, list_of_countries, list_of_russian_cities)

    text = "Привет!\nЧтобы поиграть в страны, отправь /countries\nЧтобы поиграть в русские города, отправь /russian_cities\n\nВместо буквы \"ё\" надо писать \"е\""
    await msg.answer(text, reply_markup=buttons)


@dp.message_handler(commands="countries")
async def countries(msg: types.Message):
    insert_update_table(msg.from_user.id, msg.from_user.username, list_of_countries, list_of_russian_cities)

    with sqlite3.connect("my_games.sqlite") as con:
        cur = con.cursor()
        cur.execute("UPDATE users SET play_countries = ?, play_russian_cities = ? WHERE user_id = ?", (1, 0, msg.from_user.id))

    await msg.answer("введите страну")


@dp.message_handler(commands="russian_cities")
async def russian_cities(msg: types.Message):
    insert_update_table(msg.from_user.id, msg.from_user.username, list_of_countries, list_of_russian_cities)

    with sqlite3.connect("my_games.sqlite") as con:
        cur = con.cursor()
        cur.execute("UPDATE users SET play_countries = ?, play_russian_cities = ? WHERE user_id = ?", (0, 1, msg.from_user.id))
            
    await msg.answer("введите город")


@dp.message_handler()
async def play_game(msg: types.Message):
    print(msg.from_user.username, 'в play_game')

    with sqlite3.connect("my_games.sqlite") as con:
        cur = con.cursor()
        try:
            play_countries = list(cur.execute(
                "SELECT play_countries FROM users WHERE user_id = ?", (msg.from_user.id,)))[0][0]
            play_russian_cities = list(cur.execute(
                "SELECT play_russian_cities FROM users WHERE user_id = ?", (msg.from_user.id,)))[0][0]
            
            if play_countries == 1:
                await game(bot=bot, msg=msg, table='countries_game', game_mod="play_countries")

            elif play_russian_cities == 1:
                await game(bot=bot, msg=msg, table="russian_cities_game", game_mod="play_russian_cities")
            
            else:
                print(msg.from_user.username, 'ушел из play_game')
                await msg.answer("отправьте /countries , чтобы начать игру")
        except IndexError:
            await msg.answer("отправь /help")


if __name__ == "__main__":
    create_db()
    print("===== bot online =====")
    executor.start_polling(dp, skip_updates=False)  # True
