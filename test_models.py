from unittest import TestCase
from app import app
from models import db, Users

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()


class BloglyModelsTest(TestCase):

    def setUp(self):
        """ Clean up existing users. """
        Users.query.delete()

    def tearDown(self):
        """ Clean up any failed transactions """

        db.session.rollback()

    def test_get_curr_id(self):
        new_user = Users(first_name='TestFirstName',
                         last_name='TestLastName')

        db.session.add(new_user)
        db.session.commit()

        user_id = Users.get_curr_id(new_user.id)
        self.assertEqual(user_id, 1)
