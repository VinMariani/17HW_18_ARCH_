from flask import request
from flask_restx import Resource, Namespace

from app.database import db
from app.models import MovieSchema, Movie

movies_ns = Namespace('movies')

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)


@movies_ns.route('/')
class MoviesView(Resource):
    def get(self):
        director_id = request.args.get('director_id')
        genre_id = request.args.get('genre_id')
        result = Movie.query

        if director_id is not None:
            result = result.filter(Movie.director_id == director_id)
        if genre_id is not None:
            result = result.filter(Movie.genre_id == genre_id)
        if director_id is not None and genre_id is not None:
            result = result.filter(Movie.director_id == director_id, Movie.genre_id == genre_id)

        all_movies = result.all()

        return movies_schema.dump(all_movies), 200

        # all_movies = db.session.query(Movie).all() #Возвращаю все фильмы
        # return movies_schema.dump(all_movies), 200

    def post(self):
        read_json = request.json
        new_movie = Movie(**read_json)
        with db.session.begin():  # когда выйдем из with произойдет автокоммит
            db.session.add(new_movie)
        return "", 201


@movies_ns.route('/<int:mid>')
class MovieView(Resource):
    def get(self, mid: int):
        try:
            film = db.session.query(Movie).filter(Movie.id == mid).one()
            # film = Movie.query.get(mid) второй способ выбора фильма по id из БД
            return movie_schema.dump(film), 200
        except Exception as nf:
            return str('Фильм не найден'), 404

    def delete(self, mid: int):
        try:
            film = db.session.query(Movie).get(mid)
            # film = Movie.query.get(mid) второй способ выбора фильма по id из БД
            db.session.delete(film)
            db.session.commit()
            return '', 204
        except Exception as nf:
            return str('Фильм не найден'), 404

    def put(self, mid: int):  # замена данных
        movie = db.session.query(Movie).get(mid)
        read_json = request.json

        movie.title = read_json.get('title')
        movie.description = read_json.get('description')
        movie.trailer = read_json.get('trailer')
        movie.year = read_json.get('year')
        movie.rating = read_json.get('rating')

        db.session.add(movie)
        db.session.commit()

        return '', 204
