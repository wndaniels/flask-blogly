"""Blogly application."""

from flask import Flask, current_app, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Users, Post

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


@app.errorhandler(404)
def page_not_found(e):
    """Show 404 NOT FOUND page."""

    return render_template('/user/404.html'), 404


@app.route('/users')
def users_page():
    """ Show all users"""
    user_info = Users.query.all()
    return render_template('/user/user_list.html', user=user_info)


@app.route('/users/new')
def new_user():
    """ Show form for adding new user """
    return render_template('/user/new_user.html')


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
    return render_template("/user/user_details.html", user=user)


@ app.route('/users/<int:users_id>/edit')
def edit_user(users_id):
    """ Show form allowing User to edit their info """
    user = Users.get_curr_by_id(users_id)
    return render_template('/user/edit_user.html', user=user)


@ app.route('/users/<int:users_id>/edit', methods=['POST'])
def edit_user_info(users_id):
    """ Edit users info, and update in list """

    user = Users.query.get_or_404(users_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect(f"/users/{users_id}")


@ app.route('/users/<int:users_id>/delete', methods=["POST"])
def delete_user(users_id):
    """ Delete users from list """

    user = Users.query.get_or_404(users_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')


@ app.route('/users/<int:users_id>/post-form')
def user_post_form(users_id):
    """ Show form allowing User to create a new post """

    user = Users.get_curr_by_id(users_id)
    return render_template('/post/new_post.html', user=user)


@ app.route('/users/<int:users_id>/post-form', methods=['POST'])
def user_post_new(users_id):
    """ Show form allowing User to create a new post """

    user = Users.query.get_or_404(users_id)
    new_post = Post(title=request.form['title'],
                    content=request.form['content'],
                    users_id=users_id)

    db.session.add(new_post)
    db.session.commit()

    return redirect(f"/users/{user.id}/post/{new_post.id}")


@ app.route('/users/<int:users_id>/post/<int:post_id>')
def user_post(users_id, post_id):
    """ Show Users post details"""
    user = Users.query.get_or_404(users_id)
    post = Post.query.get_or_404(post_id)
    return render_template('/post/post_details.html', user=user, post=post)


@app.route('/posts/<int:post_id>/edit')
def posts_edit(post_id):
    """Show a form to edit an existing post"""

    post = Post.query.get_or_404(post_id)
    return render_template('/post/edit_post.html', post=post)


@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def posts_update(post_id):
    """Handle form submission for updating an existing post"""

    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    db.session.add(post)
    db.session.commit()
    flash(f"Post '{post.title}' edited.")

    return redirect(f"/users/{post.users_id}/post/{post.id}")


@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def posts_destroy(post_id):
    """Handle form submission for deleting an existing post"""

    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()

    return redirect(f"/users/{post.users_id}")
