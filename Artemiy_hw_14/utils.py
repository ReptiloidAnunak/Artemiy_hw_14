import sqlite3


#Структура таблицы

"""| show_id | type | title | director | cast | country | date_added | release_year | rating | duration | duration_type | listed_in | description """



def search_by_title_fresh (word, data_base='netflix.db'):
    """Принимает название и возвращает данные в формате
    {
        "title": "title",
        "country": "country",
        "release_year": 2021,
        "genre": "listed_in",
        "description": "description"
    }"""
    with sqlite3.connect(data_base) as connection:
        cursor = connection.cursor()

        sqlite_query = f"""SELECT title, country, release_year, listed_in, description
                           FROM netflix
                           WHERE title LIKE '%{word}%'
                           ORDER BY release_year DESC
                           LIMIT 1
                        """

        cursor.execute(sqlite_query)
        film = cursor.fetchone()
        result = {"title": film[0],
              "country": film[1],
              "release_year": film[2],
              "genre": film[3],
              "description": film[4]
                     }
    return dict(result)


def search_by_years (year_from, year_to, data_base='netflix.db'):
    """Принимает два года-значения и возвращает список словарей
    с релевантными фильмами {"title":"title", "release_year": 2021}"""

    with sqlite3.connect(data_base) as connection:
        cursor = connection.cursor()
        found_films = []
        sqlite_query = \
            f"""
        SELECT title, release_year
        FROM netflix
        WHERE release_year BETWEEN {year_from} AND {year_to}    
        ORDER BY release_year DESC
        LIMIT 100
        """
        cursor.execute(sqlite_query)
        films = cursor.fetchall()

        for film in films:
            converted_film = {"title": film[0], "release_year": film[1]}
            found_films.append(converted_film)

        return found_films

def seach_by_rating(level, data_base='netflix.db'):
    """Принимает список допустимых рейтингов и возвращает данные в том же формате
         {
        "title": "title",
        "country": "country",
        "release_year": 2021,
        "genre": "listed_in",
        "description": "description"
    }"""
    level = level.upper()
    if level not in ["G", "PG", "PG-13", "R", "NC-17", "NR"]:
        return "ERROR: This level does not exist"

    if level == "R" and level != "NR":
        with sqlite3.connect(data_base) as connection:
            cursor = connection.cursor()
            found_films = []
            sqlite_query = \
                f"""
                SELECT title, country, release_year, listed_in, description, rating
                FROM netflix
                WHERE rating='{level}'
                LIMIT 20
                """

            cursor.execute(sqlite_query)
            films = cursor.fetchall()

            for film in films:
                converted_film = {"title": film[0],
                                  "country": film[1],
                                  "release_year": film[2],
                                  "genre": film[3],
                                  "description": film[4]}

                print(film[5])
                found_films.append(converted_film)

            return found_films
    else:

        with sqlite3.connect(data_base) as connection:
            cursor = connection.cursor()
            found_films = []
            sqlite_query = \
                f"""
                SELECT title, country, release_year, listed_in, description, rating
                FROM netflix
                WHERE rating LIKE '%{level}%'
                LIMIT 20
                """

            cursor.execute(sqlite_query)
            films = cursor.fetchall()

            for film in films:
                converted_film = {"title": film[0],
                                  "country": film[1],
                                  "release_year": film[2],
                                  "genre": film[3],
                                  "description": film[4]}

                print(film[5])
                found_films.append(converted_film)

            return found_films


    if level == "G":
        with sqlite3.connect(data_base) as connection:
            cursor = connection.cursor()
            found_films = []
            sqlite_query = \
                f"""
            SELECT title, country, release_year, listed_in, description, rating
            FROM netflix
            WHERE rating='{level}' AND rating!=PG AND rating!=PG-13
            LIMIT 20
            """

            cursor.execute(sqlite_query)
            films = cursor.fetchall()

            for film in films:
                converted_film = {"title": film[0],
                                  "country": film[1],
                                  "release_year": film[2],
                                  "genre": film[3],
                                  "description": film[4]}

                print(film[5])
                found_films.append(converted_film)

            return found_films
    else:

        with sqlite3.connect(data_base) as connection:
            cursor = connection.cursor()
            found_films = []
            sqlite_query = \
                f"""
            SELECT title, country, release_year, listed_in, description, rating
            FROM netflix
            WHERE rating LIKE '%{level}%'
            LIMIT 20
            """

            cursor.execute(sqlite_query)
            films = cursor.fetchall()


            for film in films:
                converted_film = {"title": film[0],
                  "country": film[1],
                  "release_year": film[2],
                  "genre": film[3],
                  "description": film[4]}

                print(film[5])
                found_films.append(converted_film)

            return found_films


def search_by_genre(genre):
    """Получает название жанра в качестве аргумента и возвращает 10 самых свежих фильмов в формате json"""

    with sqlite3.connect(database="netflix.db") as connection:
        cursor = connection.cursor()
        found_films = []
        sqlite_query = \
        f"""
        SELECT title, country, release_year, listed_in, description, rating, date_added
        FROM netflix
        WHERE listed_in LIKE '%{genre}%'
        ORDER BY date_added DESC
        LIMIT 10
        """
        cursor.execute(sqlite_query)
        films = cursor.fetchall()

        for film in films:
            converted_film = {"title": film[0],
                              "description": film[4]}

            print(film[6])

            found_films.append(converted_film)

        return found_films


def actors_pares(name_1, name_2):
    """Получает в качестве аргумента имена двух актеров, сохраняет всех актеров из колонки cast и возвращает список тех, кто играет с ними в паре больше 2 раз"""

    with sqlite3.connect(database="netflix.db") as connection:
        cursor = connection.cursor()
        sqlite_query_all_actors = \
        f"""
        SELECT "cast"
        FROM netflix
        WHERE netflix."cast" LIKE '%{name_1}%' AND netflix."cast" LIKE '%{name_2}%'
        """
        cursor.execute(sqlite_query_all_actors)
        all_actors = cursor.fetchall()

        actors_with_pare = []
        actors_more_than_2 = []
        for item in all_actors:
            for actors in item:
                film_actors = actors.split(", ")
                for actor in film_actors:
                    if actor != name_1 and actor != name_2:
                        actors_with_pare.append(actor)

        for actor in actors_with_pare:
            if actors_with_pare.count(actor) > 2 and actor not in actors_more_than_2:
                actors_more_than_2.append(actor)

    return actors_more_than_2



print("\n")
print(actors_pares("Rose McIver", "Ben Lamb"))
print("\n")
print(actors_pares("Jack Black", "Dustin Hoffman"))



