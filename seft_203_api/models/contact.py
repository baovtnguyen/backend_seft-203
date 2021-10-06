from seft_203_api.db import db


class ContactModel(db.Model):
    __tablename__ = "contacts"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    title = db.Column(db.String(80), unique=True, nullable=False)
    department = db.Column(db.String(80), nullable=False)
    project = db.Column(db.String(80), nullable=False)
    avatar = db.Column(db.String(80), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def __init__(self, first_name, last_name, title, department, project, avatar, user_id):
        self.first_name = first_name
        self.last_name = last_name
        self.title = title
        self.department = department
        self.project = project
        self.avatar = avatar
        self.user_id = user_id
        

    def json(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "title": self.title,
            "department": self.department,
            "project": self.project,
            "avatar": self.avatar,
            "user_id": self.user_id,
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def update_to_db(self):
        db.session.commit()

    @classmethod
    def find_all(cls):
        return cls.query.all()
    
    @classmethod
    def find_all_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()

    @classmethod
    def find_one_by_id(cls, _id, user_id=None):
        if user_id:
            return cls.query.filter_by(id=_id, user_id=user_id).first()
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_one_by_title(cls, title, user_id=None):
        if user_id:
            return cls.query.filter_by(title=title, user_id=user_id).first()
        return cls.query.filter_by(title=title).first()

    @classmethod
    def search_by_keyword(cls, keyword, user_id=None):
        if user_id:
            return cls.query.filter_by(user_id=user_id).filter(cls.title.contains(keyword)).all()
        return cls.query.filter(cls.title.contains(keyword)).all()