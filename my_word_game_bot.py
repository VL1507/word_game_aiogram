import sqlite3
from random import choice
from aiogram import Bot, Dispatcher, types, executor


bot = Bot(token='',
          parse_mode="HTML")
dp = Dispatcher(bot=bot)


list_of_countries = ['Австралия', 'Австрия', 'Азербайджан', 'Албания', 'Алжир', 'Ангола', 'Андорра', 'Антигуа и Барбуда', 'Аргентина',
                     'Армения', 'Афганистан', 'Багамы', 'Бангладеш', 'Барбадос', 'Бахрейн', 'Белоруссия', 'Белиз', 'Бельгия', 'Бенин',
                     'Болгария', 'Боливия', 'Босния и Герцеговина', 'Ботсвана', 'Бразилия', 'Бруней', 'Буркина-Фасо', 'Бурунди', 'Бутан',
                     'Вануату', 'Великобритания', 'Венгрия', 'Венесуэла', 'Восточный Тимор', 'Вьетнам', 'Габон', 'Гаити', 'Гайана', 'Гамбия',
                     'Гана', 'Гватемала', 'Гвинея', 'Гвинея-Бисау', 'Германия', 'Гондурас', 'Гренада', 'Греция', 'Грузия', 'Дания', 'Джибути',
                     'Доминика', 'Доминикана', 'Египет', 'Замбия', 'Зимбабве', 'Израиль', 'Индия', 'Индонезия', 'Иордания', 'Ирак', 'Иран',
                     'Ирландия', 'Исландия', 'Испания', 'Италия', 'Йемен', 'Кабо-Верде', 'Казахстан', 'Камбоджа', 'Камерун', 'Канада',
                     'Катар', 'Кения', 'Кипр', 'Киргизия', 'Кирибати', 'Китай', 'Колумбия', 'Коморы', 'Конго', 'ДР Конго', 'КНДР', 'Корея',
                     'Коста-Рика', 'Кот-д’Ивуар', 'Куба', 'Кувейт', 'Лаос', 'Латвия', 'Лесото', 'Либерия', 'Ливан', 'Ливия', 'Литва',
                     'Лихтенштейн', 'Люксембург', 'Маврикий', 'Мавритания', 'Мадагаскар', 'Малави', 'Малайзия', 'Мали', 'Мальдивы',
                     'Мальта', 'Марокко', 'Маршалловы Острова', 'Мексика', 'Микронезия', 'Мозамбик', 'Молдавия', 'Монако', 'Монголия',
                     'Мьянма', 'Намибия', 'Науру', 'Непал', 'Нигер', 'Нигерия', 'Нидерланды', 'Никарагуа', 'Новая Зеландия', 'Норвегия',
                     'ОАЭ', 'Оман', 'Пакистан', 'Палау', 'Панама', 'Папуа-Новая Гвинея', 'Парагвай', 'Перу', 'Польша', 'Португалия',
                     'Россия', 'Руанда', 'Румыния', 'Сальвадор', 'Самоа', 'Сан-Марино', 'Сан-Томе и Принсипи', 'Саудовская Аравия',
                     'Северная Македония', 'Сейшелы', 'Сенегал', 'Сент-Винсент и Гренадины', 'Сент-Китс и Невис', 'Сент-Люсия',
                     'Сербия', 'Сингапур', 'Сирия', 'Словакия', 'Словения', 'США', 'Соломоновы Острова', 'Сомали', 'Судан', 'Суринам',
                     'Сьерра-Леоне', 'Таджикистан', 'Таиланд', 'Танзания', 'Того', 'Тонга', 'Тринидад и Тобаго', 'Тувалу', 'Тунис',
                     'Туркмения', 'Турция', 'Уганда', 'Узбекистан', 'Украина', 'Уругвай', 'Фиджи', 'Филиппины', 'Финляндия', 'Франция',
                     'Хорватия', 'ЦАР', 'Чад', 'Черногория', 'Чехия', 'Чили', 'Швейцария', 'Швеция', 'Шри-Ланка', 'Эквадор',
                     'Экваториальная Гвинея', 'Эритрея', 'Эсватини', 'Эстония', 'Эфиопия', 'ЮАР', 'Южный Судан', 'Ямайка', 'Япония']


start_countries = False


@dp.message_handler(commands=["start", "help"])
async def start_help(msg: types.Message):
    print(msg.from_user.username, 'в start_help')

    global start_countries
    start_countries = False

    insert_update_table(
        msg.from_user.id, msg.from_user.username, list_of_countries)

    text = "Привет!\nЧтобы поиграть в страны, отправь /countries"
    await msg.answer(text)

    print('start_help finished')


@dp.message_handler(commands="countries")
async def countries(msg: types.Message):
    print(msg.from_user.username, 'в countries')

    global start_countries
    start_countries = True

    insert_update_table(
        msg.from_user.id, msg.from_user.username, list_of_countries)

    await msg.answer("введите страну")


@dp.message_handler()
async def play_countries(msg: types.Message):
    global start_countries
    print(msg.from_user.username, 'в play_countries')

    if start_countries == True:
        print(msg.text)

        with sqlite3.connect("my_games.sqlite") as con:
            cur = con.cursor()

            last_letter = list(cur.execute(f"SELECT last_letter FROM countries_game WHERE user_id = '{msg.from_user.id}'"))[0][0].upper()
            print(last_letter)

            used_words = []
            for i in cur.execute(f"SELECT used_words FROM countries_game WHERE user_id = '{msg.from_user.id}'"):
                used_words.append(i[0].replace('_', ' '))
            used_words = used_words[0].split()
            if msg.text not in used_words:
                bot_lst = []
                for i in cur.execute(f"SELECT bot_lst FROM countries_game WHERE user_id = '{msg.from_user.id}'"):
                    # bot_lst.append(i[0].replace('_', ' '))
                    bot_lst.append(i[0])
                bot_lst = bot_lst[0].split('_')
                if msg.text in bot_lst:
                    bot_lst.remove(msg.text)
                    used_words.append(msg.text)
                    if msg.text[0] == last_letter or last_letter == "Q":
                        print(used_words)
                        last_letter = msg.text.replace(
                            'ь', '').replace('ы', '')[-1].upper()
                        if len([i for i in bot_lst if i[0] == last_letter]) != 0:

                            bot_country = choice([i for i in bot_lst if i[0] == last_letter])
                            bot_lst.remove(bot_country)
                            used_words.append(bot_country)
                            last_letter = bot_country.replace('ь', '').replace('ы', '')[-1].upper()
                            cur.execute(f"""UPDATE countries_game SET bot_lst = '{"_".join(bot_lst)}', used_words = '{"_".join(used_words)}', last_letter = '{last_letter}' WHERE user_id = {msg.from_user.id}""")
                            # await bot.send_message(msg.from_user.id, bot_country)
                            print(used_words)
                            await bot.send_message(chat_id=msg.from_user.id, text=bot_country, reply_to_message_id=msg.message_id)
                            
                            if len([i for i in bot_lst if i[0] == last_letter]) == 0:
                                start_countries = False
                                await msg.answer(f"Бот победил. больше нет слов на <b>{last_letter}</b>")

                        else:
                            text = "Поздравляю! Ты победил!"
                            start_countries = False
                            await bot.send_message(chat_id=msg.from_user.id, text=text, reply_to_message_id=msg.message_id)
                    else:
                        text = f'надо, чтобы слово начиналось на <b>{last_letter}</b>'
                        await bot.send_message(chat_id=msg.from_user.id, text=text, reply_to_message_id=msg.message_id)
                else:
                    await msg.answer("я не знаю такой страны :(\nпопробуй ввести другую")
            else:
                await msg.answer("такая страна уже была\nпопробуй ввести другую")

    else:
        print(msg.from_user.username, 'ушел из play_countries')
        await msg.answer("отправьте /countries , чтобы начать игру")


def create_db() -> None:
    """создает базу данных my_games.sqlite и
    таблицы countries_game и cities_game"""

    with sqlite3.connect("my_games.sqlite") as con:
        cur = con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS countries_game (
        user_id INT,
        username TEXT,
        bot_lst TEXT,
        used_words TEXT,
        last_letter TEXT
        )""")

        # cur.execute("""CREATE TABLE IF NOT EXISTS cities_game (
        # user_id INT,
        # username TEXT,
        # bot_lst TEXT,
        # used_words TEXT
        # )""")

        print("<<<<< db создана >>>>>")


def insert_update_table(userid: int, username: str, list_of_countries: list) -> None:
    """'обнуляет' или создает запись о человеке в countries_game

    Args:
        userid (int): id человека
        username (str): имя человека
        list_of_countries (list): список стран
    """
    with sqlite3.connect("my_games.sqlite") as con:
        cur = con.cursor()

        if (userid,) not in list(cur.execute("SELECT user_id FROM countries_game")):

            cur.execute("""INSERT INTO countries_game VALUES (?, ?, ?, ?, ?)""",
                        (userid, username, "_".join(list_of_countries), "_", 'q'))
        else:
            cur.execute(
                f"""UPDATE countries_game SET bot_lst = '{"_".join(list_of_countries)}', used_words = '_', last_letter = 'q' WHERE user_id  = {userid}""")


if __name__ == "__main__":
    create_db()
    print("===== bot online =====")
    executor.start_polling(dp, skip_updates=False)  # True
