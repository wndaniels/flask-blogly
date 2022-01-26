from unittest import TestCase

from app import app
from models import db, Users

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class UsersTestCase(TestCase):
    """Tests for views for Pets."""

    def setUp(self):
        """Add sample pet."""

        Users.query.delete()

        new_user = Users(first_name='TestFirstName',
                         last_name='TestLastName')
        db.session.add(new_user)
        db.session.commit()

        self.new_user_id = new_user.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_user_list_redir(self):
        with app.test_client() as client:
            res = client.get("/", follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('TestFirstName', html)

    def test_show_user_data(self):
        with app.test_client() as client:
            res = client.get(f"/users/{self.new_user_id}")
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1>TestFirstName TestLastName</h1>', html)

    def test_add_user(self):
        with app.test_client() as client:
            new_user = {"first_name": "TestFirstName",
                        "last_name": "TestLastName", "image_url": "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png"}
            res = client.post(
                "/users/new", data=new_user, follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('TestFirstName', html)

    def test_delete_user(self):
        with app.test_client() as client:
            user = {"first_name": "TestFirstName",
                    "last_name": "TestLastName", "image_url": "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png"}
            res = client.post(
                f"/users/{self.new_user_id}/delete", data=user, follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertNotIn('TestFirstName', html)
