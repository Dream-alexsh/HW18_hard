from flask_restx import Resource, Namespace
from sqlalchemy.exc import NoResultFound

from container import genre_service
from dao.models.genres import GenreSchema


genre_ns = Namespace('genres')
genres_schema = GenreSchema(many=True)
genre_schema = GenreSchema()


@genre_ns.route('/')
class GenresView(Resource):
    def get(self):
        genres = genre_service.get_all()
        return genres_schema.dump(genres), 200



@genre_ns.route('/<int:bid>')
class GenreView(Resource):
    def get(self, bid: int):
        try:
            genre = genre_service.get_one(bid)
            return genre_schema.dump(genre), 200
        except NoResultFound as e:
            return str(e), 404
