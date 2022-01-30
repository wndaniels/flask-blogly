"""Models for Blogly."""

import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)


DEFAULT_USER_IMAGE = "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png"


class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text, nullable=True, default=DEFAULT_USER_IMAGE)

    posts = db.relationship("Post", backref="users",
                            cascade="all, delete-orphan")

    @classmethod
    def get_curr_by_id(cls, id):
        return cls.query.filter_by(id=id).all()


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.datetime.now)
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    @property
    def date_time(self):
        """Return nicely-formatted date."""

        return self.created_at.strftime("%b %-d  %Y, %-I:%M %p")

    @classmethod
    def get_curr_post_by_id(cls, id):
        return cls.query.filter_by(id=id).all()
