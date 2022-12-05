import sqlite3


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

        # cur.execute("""CREATE TABLE IF NOT EXISTS cities_game (
        # user_id INT,
        # username TEXT,
        # bot_lst TEXT,
        # used_words TEXT
        # )""")

        print("<<<<< db создана >>>>>")


def insert_update_table(userid: int, username: str, list_of_countries: list, list_of_russian_cities: list) -> None:
    """'обнуляет' или создает запись о человеке в countries_game

    Args:
        userid (int): id человека
        username (str): имя человека
        list_of_countries (list): список стран
    """
    with sqlite3.connect("my_games.sqlite") as con:
        cur = con.cursor()

        #
        if (userid,) not in list(cur.execute("SELECT user_id FROM countries_game")):

            cur.execute("INSERT INTO countries_game VALUES (?, ?, ?, ?, ?)",
                        (userid, username, "_".join(list_of_countries), "_", 'KOSTYL'))
        else:
            cur.execute(
                "UPDATE countries_game SET bot_lst = ?, used_words = ?, last_letter = ? WHERE user_id  = ?", ("_".join(list_of_countries), '_', 'KOSTYL', userid))

        #
        if (userid,) not in list(cur.execute("SELECT user_id FROM russian_cities_game")):

            cur.execute("INSERT INTO russian_cities_game VALUES (?, ?, ?, ?, ?)",
                        (userid, username, "_".join(list_of_russian_cities), "_", 'KOSTYL'))
        else:
            cur.execute(
                "UPDATE russian_cities_game SET bot_lst = ?, used_words = ?, last_letter = ? WHERE user_id  = ?", ("_".join(list_of_russian_cities), '_', 'KOSTYL', userid))

        #
        if (userid,) not in list(cur.execute("SELECT user_id FROM users")):

            cur.execute("INSERT INTO users VALUES (?, ?, ?, ?)",
                        (userid, username, 0, 0))
        else:
            cur.execute(
                "UPDATE users SET play_countries = ?, play_russian_cities = ? WHERE user_id  = ?", (0, 0, userid))
