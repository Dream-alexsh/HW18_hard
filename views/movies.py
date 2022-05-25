from flask import request, jsonify
from flask_restx import Resource, Namespace
from marshmallow import ValidationError
from sqlalchemy.exc import NoResultFound

from container import movie_service
from dao.models.movies import MovieSchema


movie_ns = Namespace('movies')

movies_schema = MovieSchema(many=True)
movie_schema = MovieSchema()


@movie_ns.route('/')
class MoviesView(Resource):
    def get(self):
        year = request.args.get('year')
        director_id = request.args.get('director_id')
        genre_id = request.args.get('genre_id')
        if year:
            all_movies = movie_service.get_by_year(year)
        elif director_id:
            all_movies = movie_service.get_by_director(director_id)
        elif genre_id:
            all_movies = movie_service.get_by_genre(genre_id)
        else:
            all_movies = movie_service.get_all()
        return movies_schema.dump(all_movies)


    def post(self):
        req_json = request.get_json()
        try:
            req_json = movie_schema.load(req_json)
        except ValidationError as e:
            return f"{e}", 400
        movie_id = req_json['id']
        movie_service.create(req_json)
        response = jsonify()
        response.status_code = 201
        response.headers['location'] = f'/{movie_id}'

        return response


@movie_ns.route('/<int:bid>')
class MovieView(Resource):
    def get(self, bid: int):
        try:
            movie = movie_service.get_one(bid)
            return movie_schema.dump(movie), 200
        except NoResultFound as e:
            return str(e), 404

    def put(self, bid: int):
        req_json = request.get_json()
        try:
            req_json = movie_schema.load(req_json)
        except ValidationError as e:
            return f"{e}", 400
        req_json['id'] = bid
        movie_service.update(req_json)

        return "", 204

    def patch(self, bid: int):
        req_json = request.get_json()
        try:
            req_json = movie_schema.load(req_json)
        except ValidationError as e:
            return f"{e}", 400
        req_json['id'] = bid
        movie_service.update_partial(req_json)

        return "", 204

    def delete(self, bid: int):
        movie_service.delete(bid)

        return "", 204
