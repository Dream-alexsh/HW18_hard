from dao.models.directors import Director


class DirectorDAO:
    def __init__(self, session):
        self.session = session

    def get_all(self):
        return self.session.query(Director).all()

    def get_one(self, mid):
        return self.session.query(Director).filter(Director.id == mid).one()

