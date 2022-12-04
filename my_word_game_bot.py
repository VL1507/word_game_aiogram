import sqlite3
from random import choice
from aiogram import Bot, Dispatcher, types, executor

from word_lists import list_of_countries, list_of_russian_cities
from keyboards import buttons


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
    with sqlite3.connect("my_games.sqlite") as con:
        cur = con.cursor()
        try:
            play_countries = list(cur.execute("SELECT play_countries FROM users WHERE user_id = ?", (msg.from_user.id,)))[0][0]
            play_russian_cities = list(cur.execute("SELECT play_russian_cities FROM users WHERE user_id = ?", (msg.from_user.id,)))[0][0]
            
            if play_countries == 1:
                last_letter = list(cur.execute("SELECT last_letter FROM countries_game WHERE user_id = ?", (msg.from_user.id,)))[0][0].upper()
                used_words = []
                    
                for i in cur.execute("SELECT used_words FROM countries_game WHERE user_id = ?", (msg.from_user.id,)):
                    used_words.append(i[0].replace('_', ' '))
                used_words = used_words[0].split()
          
                if msg.text not in used_words:
                    bot_lst = []
                    for i in cur.execute("SELECT bot_lst FROM countries_game WHERE user_id = ?", (msg.from_user.id,)):
                        bot_lst.append(i[0])
                    bot_lst = bot_lst[0].split('_')
                    
                    if msg.text in bot_lst:
                        bot_lst.remove(msg.text)
                        used_words.append(msg.text)
                              
                        if msg.text[0] == last_letter or last_letter == "KOSTYL":
                            print(used_words)
                            last_letter = msg.text.replace('ь', '').replace('ы', '')[-1].upper()
                              
                            if len([i for i in bot_lst if i[0] == last_letter]) != 0:
                                bot_country = choice(
                                    [i for i in bot_lst if i[0] == last_letter])
                                bot_lst.remove(bot_country)
                                used_words.append(bot_country)
                                last_letter = bot_country.replace('ь', '').replace('ы', '')[-1].upper()
                                cur.execute("UPDATE countries_game SET bot_lst = ?, used_words = ?, last_letter = ? WHERE user_id = ?", ("_".join(bot_lst), "_".join(used_words), last_letter, msg.from_user.id))
                                await bot.send_message(chat_id=msg.from_user.id, text=bot_country, reply_to_message_id=msg.message_id)

                                if len([i for i in bot_lst if i[0] == last_letter]) == 0:
                                    cur.execute("UPDATE users SET play_countries = ? WHERE user_id = ?", (0, msg.from_user.id))
                                    await msg.answer(f"Бот победил. больше нет слов на <b>{last_letter}</b>")
                            else:
                                text = "Поздравляю! Ты победил!"
                                cur.execute("UPDATE users SET play_countries = ? WHERE user_id = ?", (0, msg.from_user.id))
                                await bot.send_message(chat_id=msg.from_user.id, text=text, reply_to_message_id=msg.message_id)
                        else:
                            text = f'надо, чтобы слово начиналось на <b>{last_letter}</b>'
                            await bot.send_message(chat_id=msg.from_user.id, text=text, reply_to_message_id=msg.message_id)
                    else:
                        await msg.answer("я не знаю такое слово :(\nпопробуй ввести другое")
                else:
                    await msg.answer("такое слово уже было\nпопробуй ввести другое")
                    
            #---------------------------------------------------------------------------------------
          
            elif play_russian_cities == 1:
                last_letter = list(cur.execute("SELECT last_letter FROM russian_cities_game WHERE user_id = ?", (msg.from_user.id,)))[0][0].upper()
                used_words = []
                    
                for i in cur.execute("SELECT used_words FROM russian_cities_game WHERE user_id = ?", (msg.from_user.id,)):
                    used_words.append(i[0].replace('_', ' '))
                used_words = used_words[0].split()
          
                if msg.text not in used_words:
                    bot_lst = []
                    for i in cur.execute("SELECT bot_lst FROM russian_cities_game WHERE user_id = ?", (msg.from_user.id,)):
                        bot_lst.append(i[0])
                    bot_lst = bot_lst[0].split('_')
                    
                    if msg.text in bot_lst:
                        bot_lst.remove(msg.text)
                        used_words.append(msg.text)
                              
                        if msg.text[0] == last_letter or last_letter == "KOSTYL":
                            last_letter = msg.text.replace('ь', '').replace('ы', '')[-1].upper()
                    
                            if len([i for i in bot_lst if i[0] == last_letter]) != 0:
                                bot_country = choice([i for i in bot_lst if i[0] == last_letter])
                                bot_lst.remove(bot_country)
                                used_words.append(bot_country)
                                last_letter = bot_country.replace('ь', '').replace('ы', '')[-1].upper()
                                cur.execute("UPDATE russian_cities_game SET bot_lst = ?, used_words = ?, last_letter = ? WHERE user_id = ?", ("_".join(bot_lst), "_".join(used_words), last_letter, msg.from_user.id))
                                await bot.send_message(chat_id=msg.from_user.id, text=bot_country, reply_to_message_id=msg.message_id)
                                        
                                if len([i for i in bot_lst if i[0] == last_letter]) == 0:
                                    cur.execute("UPDATE users SET play_russian_cities = ? WHERE user_id = ?", (0, msg.from_user.id))
                                    await msg.answer(f"Бот победил. больше нет слов на <b>{last_letter}</b>")
                            else:
                                text = "Поздравляю! Ты победил!"
                                cur.execute("UPDATE users SET play_russian_cities = ? WHERE user_id = ?", (0, msg.from_user.id))
                                await bot.send_message(chat_id=msg.from_user.id, text=text, reply_to_message_id=msg.message_id)
                        else:
                            text = f'надо, чтобы слово начиналось на <b>{last_letter}</b>'
                            await bot.send_message(chat_id=msg.from_user.id, text=text, reply_to_message_id=msg.message_id)
                    else:
                        await msg.answer("я не знаю такое слово :(\nпопробуй ввести другое")
                else:
                    await msg.answer("такое слово уже было\nпопробуй ввести другое")
            
            #---------------------------------------------------------------------------------------
                    
            else:
                await msg.answer("отправьте /countries , чтобы начать игру")
        except IndexError:
            await msg.answer("отправь /help")
      
                    
def game():
    ...


def create_db() -> None:
    """создает базу данных my_games.sqlite и
    таблицы countries_game и cities_game"""

    with sqlite3.connect("my_games.sqlite") as con:
        cur = con.cursor()

        cur.execute("""CREATE TABLE IF NOT EXISTS users (
        user_id INT,
        username TEXT,
        play_countries INT,
        play_russian_cities INT
        )""")

        cur.execute("""CREATE TABLE IF NOT EXISTS countries_game (
        user_id INT,
        username TEXT,
        bot_lst TEXT,
        used_words TEXT,
        last_letter TEXT
        )""")

        cur.execute("""CREATE TABLE IF NOT EXISTS russian_cities_game (
        user_id INT,
        username TEXT,
        bot_lst TEXT,
        used_words TEXT,
        last_letter TEXT
        )""")
        
        print("<<<<< db создана >>>>>")


def insert_update_table(userid: int, username: str, list_of_countries: list, list_of_russian_cities: list) -> None:
    """'обнуляет' или создает запись о человеке в countries_game"""

    with sqlite3.connect("my_games.sqlite") as con:
        cur = con.cursor()
        
        #
        if (userid,) not in list(cur.execute("SELECT user_id FROM countries_game")):
            cur.execute("INSERT INTO countries_game VALUES (?, ?, ?, ?, ?)", (userid, username, "_".join(list_of_countries), "_", 'KOSTYL'))
        else:
            cur.execute("UPDATE countries_game SET bot_lst = ?, used_words = ?, last_letter = ? WHERE user_id  = ?", ("_".join(list_of_countries), '_', 'KOSTYL', userid))
            
        #
        if (userid,) not in list(cur.execute("SELECT user_id FROM russian_cities_game")):
            cur.execute("INSERT INTO russian_cities_game VALUES (?, ?, ?, ?, ?)", (userid, username, "_".join(list_of_russian_cities), "_", 'KOSTYL'))
        else:
            cur.execute("UPDATE russian_cities_game SET bot_lst = ?, used_words = ?, last_letter = ? WHERE user_id  = ?", ("_".join(list_of_russian_cities), '_', 'KOSTYL', userid))
            
        #
        if (userid,) not in list(cur.execute("SELECT user_id FROM users")):
            cur.execute("INSERT INTO users VALUES (?, ?, ?, ?)", (userid, username, 0, 0))
        else:
            cur.execute("UPDATE users SET play_countries = ?, play_russian_cities = ? WHERE user_id  = ?", (0, 0, userid))


if __name__ == "__main__":
    create_db()
    print("===== bot online =====")
    executor.start_polling(dp, skip_updates=False)  # True
