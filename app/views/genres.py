from flask import request
from flask_restx import Resource, Namespace

from app.database import db
from app.models import GenreSchema, Genre

genres_ns = Namespace('genres')

genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)


@genres_ns.route('/')
class GenresView(Resource):
    def post(self, gid: int):
        read_json = request.json
        new_genre = Genre(**read_json)
        with db.session.begin():
            db.session.add(new_genre)
        return "", 201


@genres_ns.route('/<int:gid>')
class GenresView(Resource):
    def put(self, gid: int):
        genre = db.session.query(Genre).get(gid)
        read_json = request.json

        genre.id = read_json.get('id')
        genre.name = read_json.get('name')

        db.session.add(genre)
        db.session.commit()

        return '', 204

    def delete(self, gid: int):
        try:
            genre = db.session.query(Genre).get(gid)
            db.session.delete(genre)
            db.session.commit()
        except Exception as nf:
            return str('Жанр не найден'), 404
