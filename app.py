"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Users

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "yupp1234"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route('/')
def users_page():
    """ Show users data """
    user_info = Users.query.all()
    return render_template('user_list.html', user_info=user_info)


@app.route('/new-user-form')
def new_user():
    """ Show form for adding new user """
    return render_template('new_user.html')


@app.route('/edit-user-info')
def edit_user():
    """ Show form allowing User to edit their info """
    user_info = Users.query.all()
    return render_template('edit_user.html', user_info=user_info)


@app.route('/<int:user_id>')
def show_pet(user_id):
    """ Show details of selected pet """
    user = Users.query.get_or_404(user_id)
    return render_template("user_details.html", user=user)
