from seft_203_api.db import db


class TaskModel(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(80), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    is_completed = db.Column(db.Boolean, default=False, nullable=False)

    def __init__(self, task, is_completed, user_id):
        self.task = task
        self.is_completed = is_completed
        self.user_id = user_id

    def json(self):
        return {
            "id": self.id,
            "task": self.task,
            "is_completed": self.is_completed,
            "user_id": self.user_id,
        }

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
        

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
    def find_one_by_id(cls, task_id, user_id=None):
        if user_id:
            return cls.query.filter_by(id=task_id, user_id=user_id).first()
        return cls.query.filter_by(id=task_id).first()

    @classmethod
    def find_all_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()

    @classmethod
    def find_one_by_taskname(cls, taskname, user_id=None):
        if user_id:
            return cls.query.filter_by(task=taskname, user_id=user_id).first()
        return cls.query.filter_by(task=taskname).first()

    @classmethod
    def search_by_keyword(cls, keyword, user_id=None):
        if user_id:
            return cls.query.filter_by(user_id=user_id).filter(cls.task.contains(keyword)).all()
        return cls.query.filter(cls.task.contains(keyword)).all()