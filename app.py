"""Blogly application."""

from flask import Flask, current_app, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Users, Post, Tag, PostTag

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "yupp1234"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


#################################################################
# User Form and User Details
#################################################################

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


#################################################################
# Post Form and Post Details
#################################################################

@ app.route('/users/<int:users_id>/post/new')
def user_post_form(users_id):
    """ Show form allowing User to create a new post """

    user = Users.get_curr_by_id(users_id)
    tags = Tag.query.all()
    return render_template('/post/new_post.html', user=user, tags=tags)


@ app.route('/users/<int:users_id>/post/new', methods=['POST'])
def user_post_new(users_id):
    """ Show form allowing User to create a new post """

    user = Users.query.get_or_404(users_id)
    tag_id = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_id)).all()

    new_post = Post(title=request.form['title'],
                    content=request.form['content'],
                    users_id=users_id,
                    tags=tags)

    db.session.add(new_post)
    db.session.commit()

    return redirect(f"/users/{user.id}/post/{new_post.id}")


@ app.route('/users/<int:users_id>/post/<int:post_id>')
def user_post(users_id, post_id):
    """ Show Users post details"""
    user = Users.query.get_or_404(users_id)
    post = Post.query.get_or_404(post_id)

    return render_template('/post/post_details.html', user=user, post=post)


@ app.route('/posts/<int:post_id>/edit')
def posts_edit(post_id):
    """Show a form to edit an existing post"""

    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    return render_template('/post/edit_post.html', post=post, tags=tags)


@ app.route('/posts/<int:post_id>/edit', methods=["POST"])
def posts_update(post_id):
    """Handle form submission for updating an existing post"""

    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    tag_id = [int(num) for num in request.form.getlist("tags")]
    post.tags = Tag.query.filter(Tag.id.in_(tag_id)).all()

    db.session.add(post)
    db.session.commit()

    return redirect(f"/users/{post.users_id}/post/{post.id}")


@ app.route('/posts/<int:post_id>/delete', methods=["POST"])
def posts_delete(post_id):
    """ Handle form submission for deleting an existing post """

    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()

    return redirect(f"/users/{post.users_id}")


#################################################################
# Tag Form and Tag Details
#################################################################

@ app.route('/tags')
def tags_list():
    """ Lists all tags, with links to the tag detail page. """
    tag_names = Tag.query.all()
    return render_template('/tag/tag_list.html', tag_names=tag_names)


@ app.route('/tags/new')
def new_tag():
    """ Shows a form to add a new tag. """
    return render_template('/tag/new_tag.html')


@ app.route('/tags/new', methods=['POST'])
def create_new_tag():
    """ Process add form, adds tag, and redirect to tag list. """
    new_tag = Tag(name=request.form['name'])

    db.session.add(new_tag)
    db.session.commit()

    return redirect("/tags")


@ app.route('/tags/<int:tag_id>')
def tag_post(tag_id):
    """ Show detail about a tag. Have links to edit form and to delete. """
    tag = Tag.query.get_or_404(tag_id)
    return render_template("/tag/tag_post.html", tag=tag)


@ app.route('/tags/<int:tag_id>/edit')
def edit_tag(tag_id):
    """ Show form to edit tag name. """
    tag = Tag.query.get_or_404(tag_id)
    return render_template("/tag/edit_tag.html", tag=tag)


@ app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def tag_update(tag_id):
    """ Submit form to update tag name, and redirect user to tag_post. """

    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']

    db.session.add(tag)
    db.session.commit()

    return redirect(f"/tags/{tag.id}")


@ app.route('/tags/<int:tag_id>/delete', methods=['POST'])
def tag_delete(tag_id):
    """ Handle submission for deleting tag. Redirects to tag list. """

    tag = Tag.query.get_or_404(tag_id)

    db.session.delete(tag)
    db.session.commit()

    return redirect('/tags')
