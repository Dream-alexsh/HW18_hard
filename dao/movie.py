from dao.models.movies import Movie


class MovieDAO:
    def __init__(self, session):
        self.session = session

    def get_all(self):
        return self.session.query(Movie).all()

    def create(self, data):
        movie = Movie(**data)

        self.session.add(movie)
        self.session.commit()
        self.session.close()

        return movie

    def get_one(self, mid):
        return self.session.query(Movie).filter(Movie.id == mid).one()

    def get_by_year(self, year):
        return self.session.query(Movie).filter(Movie.year == year).all()

    def get_by_director(self, director_id):
        return self.session.query(Movie).filter(Movie.director_id == director_id).all()

    def get_by_genre(self, genre_id):
        return self.session.query(Movie).filter(Movie.genre_id == genre_id).all()

    def update(self, movie):
        self.session.add(movie)
        self.session.commit()
        self.session.close()

        return movie

    def delete(self, mid):
        movie = self.get_one(mid)

        self.session.delete(movie)
        self.session.commit()
        self.session.close()

