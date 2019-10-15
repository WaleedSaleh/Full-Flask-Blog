from flask import Blueprint, redirect, url_for, request,flash, render_template, abort
from flaskblog import db
from flask_login import current_user, login_required
from flaskblog.forms.PostForm import Posts
from flaskblog.Models.Post import Post
from flaskblog.Models.User import User

posts = Blueprint('posts',__name__,template_folder='templates')


@posts.route('/<string:username>/new/post', methods=['GET', 'POST'])
@login_required
def new_post(username):
    form = Posts()
    if form.validate_on_submit():
        post = Post(title=form.title.data, body=form.post_field.data, user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        flash('You have added the post successfully', 'success')
        return redirect(url_for('main_page.home', username=current_user.username))

    return render_template('create_post.html', title='Create Post', form=form)


@posts.route('/<string:username>/posts', strict_slashes=False)
@posts.route('/<string:username>/post/<int:post_id>', strict_slashes=False)
@login_required
def post(username, post_id=None):
    if post_id:
        post = Post.query.get_or_404(post_id)
    else:
        page = request.args.get('page', 1, type=int)
        user = User.query.filter_by(username=username).first_or_404()
        posts = Post.query.filter_by(user_id=user.id) \
            .order_by(Post.publish_date.desc()) \
            .paginate(page=page, per_page=10)
        return render_template('post.html', current_user=current_user, posts=posts)
    return render_template('post.html', current_user=current_user, post=post)


@posts.route('/<string:username>/edit/post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id, username):
    post = Post.query.get_or_404(post_id)
    form = Posts()
    if username != current_user.username and post_id != post.id:
        abort(403)
    if form.validate_on_submit():
        post.body = form.post_field.data
        post.title = form.title.data
        db.session.commit()
        flash('Your post Edited Successfully!', 'success')
        return redirect(url_for('posts.post', post_id=post.id, username=post.author.username))
    elif request.method == 'GET':
        form.title.data = post.title
        form.post_field.data = post.body

    return render_template('create_post.html', title=post.title, post=post, form=form)


@posts.route('/delete-post/<int:post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)

    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted successfully!!', 'success')
    return redirect(url_for('main_page.home', username=current_user.username))


@posts.route('/<string:username>/posts', methods=['GET'])
def user_posts(username):
    return redirect(url_for('posts.post', username=username))
