import sqlite3
from flask import redirect, url_for
from utils import search_by_title_fresh, search_by_years, seach_by_rating, search_by_genre
from flask import Flask
data_base = 'netflix.db'

app = Flask(__name__, subdomain_matching=True)

@app.route("/movie/<title>")
def get_by_title(title):
    film = search_by_title_fresh(title)
    return film

@app.route("/movie/<year_from>/to/<year_to>")
def get_by_years(year_from, year_to):
    films = search_by_years(year_from, year_to)
    return films


@app.route("/rating/<rating>")
def get_by_rating(rating):
    rating = str(rating).lower()
    found_films = seach_by_rating(rating)
    if rating == "children":
        return redirect(url_for('get_by_rating_children'))
    elif rating == "family":
        return redirect(url_for("get_by_rating_family"))
    elif rating == "adult":
        return redirect(url_for("get_by_rating_adult"))

    return found_films

@app.route("/rating/children")
def get_by_rating_children():
    with sqlite3.connect(data_base) as connection:
        cursor = connection.cursor()
        found_films = []
        sqlite_query = \
            f"""
        SELECT title, country, release_year, listed_in, description, rating
        FROM netflix
        WHERE rating='G' AND rating!='PG' AND rating!='PG-13'
        """

        cursor.execute(sqlite_query)
        films = cursor.fetchall()

        for film in films:
            converted_film = {"title": film[0],
                              "rating": film[5],
                              "description": film[4]}

            found_films.append(converted_film)
        return found_films

@app.route("/rating/family")
def get_by_rating_family():
    with sqlite3.connect(data_base) as connection:
        cursor = connection.cursor()
        found_films = []
        sqlite_query = \
            f"""
        SELECT title, country, release_year, listed_in, description, rating
        FROM netflix
        WHERE rating LIKE '%PG%' OR rating='G'
        """

        cursor.execute(sqlite_query)
        films = cursor.fetchall()

        for film in films:
            converted_film = {"title": film[0],
                              "rating": film[5],
                              "description": film[4]}

            found_films.append(converted_film)
        return found_films


@app.route("/rating/adult")
def get_by_rating_adult():
    with sqlite3.connect('netflix.db') as connection:
        cursor = connection.cursor()
        found_films = []
        sqlite_query = \
            f"""
               SELECT title, country, release_year, listed_in, description, rating
               FROM netflix
               WHERE rating='R' OR rating='NC-17'
               """

        cursor.execute(sqlite_query)
        films = cursor.fetchall()

        for film in films:
            converted_film = {"title": film[0],
                              "rating": film[5],
                              "description": film[4]}

            print(film[5])

            found_films.append(converted_film)

        return found_films

@app.route("/genre/<genre>")
def get_by_genre(genre):
    genre = str(genre).capitalize()
    return search_by_genre(genre)


if __name__ == "__main__":
        app.run(debug=1)
