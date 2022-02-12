from app import db


class User(db.Model):
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True} 
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True)
    integration_id = db.Column(db.String(100))

    def create(self, session, **kwargs):
        new = self.__class__(
            name=kwargs['name'],
            email=kwargs['email'],
            integration_id=kwargs['integration_id']
        )
        session.add(new)
        return new

    def fetch(self, session, _id):
        return session.query(self.__class__).filter_by(id=_id).first()
