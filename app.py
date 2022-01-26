"""Blogly application."""

from flask import Flask, current_app, request, render_template, redirect, flash, session
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
def home_page():
    """ Redirects to list of users """
    return redirect('/users')


@app.route('/users')
def users_page():
    """ Show all users"""
    user_info = Users.query.all()
    return render_template('user_list.html', user=user_info)


@app.route('/users/new')
def new_user():
    """ Show form for adding new user """
    return render_template('new_user.html')


@app.route('/users/new', methods=['POST'])
def create_new_user():
    """ Create new user, and add to list """
    new_user = Users(
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        image_url=request.form['image_url'] or None)

    db.session.add(new_user)
    db.session.commit()

    return redirect(f"/users/{new_user.id}")


@app.route('/users/<int:users_id>')
def show_user(users_id):
    """ Show details of selected user """
    user = Users.query.get_or_404(users_id)
    return render_template("user_details.html", user=user)


@app.route('/users/<int:users_id>/edit')
def edit_user(users_id):
    """ Show form allowing User to edit their info """
    user_info = Users.get_curr_by_id(users_id)
    return render_template('edit_user.html', user_info=user_info)


@app.route('/users/<int:users_id>/edit', methods=['POST'])
def edit_user_info(users_id):
    """ Edit users info, and update in list """

    user = Users.query.get_or_404(users_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect(f"/users/{user.id}")


@app.route('/users/<int:users_id>/delete', methods=["POST"])
def delete_user(users_id):
    """ Delete users from list """

    user = Users.query.get_or_404(users_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')
