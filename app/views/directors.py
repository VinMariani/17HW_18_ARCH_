from flask import request
from flask_restx import Resource, Namespace

from app.database import db
from app.models import DirectorSchema, Director

directors_ns = Namespace('directors')

director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)


@directors_ns.route('/')
class DirectorView(Resource):
    def post(self):
        read_json = request.json
        new_director = Director(**read_json)
        with db.session.begin():
            db.session.add(new_director)
        return '', 201


@directors_ns.route('/<int:did>')
class DirectorView(Resource):
    def put(self, did: int):
        director = db.session.query(Director).get(did)
        read_json = request.json

        director.id = read_json.get('id')
        director.name = read_json.get('name')

        db.session.add(director)
        db.session.commit()

        return '', 204

    def delete(self, did: int):
        try:
            director = db.session.query(Director).get(did)
            db.session.delete(director)
            db.session.commit()
            return '', 204
        except Exception as nf:
            return str('Режиссер не найден'), 404
