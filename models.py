"""Models for Blogly."""

from email.policy import default
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)


# MODELS GO BELOW!

class Users(db.Model):
    __tablename__ = 'users'

    def __repr__(self):
        u = self
        return f"<User id={u.id} first_name={u.first_name} last_name={u.last_name} image_url={u.image_url}>"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    first_name = db.Column(db.Text,
                           nullable=False)

    last_name = db.Column(db.Text,
                          nullable=False)

    image_url = db.Column(db.Text,
                          nullable=True,
                          default="https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png")

    # @classmethod
    # def get_by_species(cls, species):
    #     return cls.query.filter_by(species=species).all()

    # @classmethod
    # def get_hunger(cls):
    #     return cls.query.filter(Pet.hunger >= 20).all()

    # def greet(self):
    #     """ Greet with pets name and their species """
    #     return f"Hi, I am {self.name} the {self.species}"

    # def feed(self, amt=20):
    #     """ Update hunger level based off of amt """
    #     self.hunger -= amt
    #     self.hunger = max(self.hunger, 0)
