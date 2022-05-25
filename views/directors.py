from flask_restx import Resource, Namespace
from sqlalchemy.exc import NoResultFound

from container import director_service
from dao.models.directors import DirectorSchema

director_ns = Namespace('directors')
director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)


@director_ns.route('/')
class DirectorsView(Resource):
    def get(self):
        directors = director_service.get_all()
        return directors_schema.dump(directors), 200



@director_ns.route('/<int:bid>')
class DirectorView(Resource):
    def get(self, bid: int):
        try:
            director = director_service.get_one(bid)
            return director_schema.dump(director), 200
        except NoResultFound as e:
            return str(e), 404
