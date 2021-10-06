from seft_203_api.db import db


class DashboardModel(db.Model):
    __tablename__ = "dashboards"

    title = db.Column(db.String(80), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    layout_type = db.Column(db.String(80), nullable=False)

    widgets = db.Column(db.PickleType, nullable=False)
    # widgets = db.relationship("WidgetModel", lazy='select',
    #     backref=db.backref('dashboard_info', lazy='joined'))

    def __init__(self, title, layout_type, widgets, user_id):
        self.title = title
        self.layout_type = layout_type
        self.widgets = widgets
        self.user_id = user_id

    def json(self):
        return {
            "title": self.title,
            "user_id": self.user_id,
            "layout_type": self.layout_type,
            "widgets": self.widgets
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def remove_widgets(self):
        for widget in self.widgets:
            widget.delete_from_db()

    def update_to_db(self):
        db.session.commit()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_all_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()

    @classmethod
    def find_one_by_title(cls, title, user_id=None):
        if user_id:
            return cls.query.filter_by(title=title, user_id=user_id).first()
        return cls.query.filter_by(title=title).first()

    
