from seft_203_api.db import db

class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    full_name = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)

    tasks = db.relationship("TaskModel", lazy='select',
        backref=db.backref('user_info', lazy='joined'))

    contacts = db.relationship("ContactModel", lazy='select',
        backref=db.backref('user_info', lazy='joined'))

    def __init__(self, username, full_name, password):
        self.username = username
        self.full_name = full_name
        self.password = password


    def json(self):
        return {
            'id': self.id, 
            'username': self.username,
            'full_name': self.full_name,
            # "tasks": [task.as_dict() for task in self.tasks]
        }

    def as_dict(self):
        result =  {c.name: getattr(self, c.name) for c in self.__table__.columns}
        result.pop("password")
        return result


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
