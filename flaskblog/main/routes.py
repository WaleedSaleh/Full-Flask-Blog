from flask import Blueprint, render_template, request
from flaskblog.Models.Post import Post
from flaskblog.forms.PostForm import Posts
from flask_login import login_required


main_page = Blueprint('main_page', __name__,template_folder='templates')


@main_page.route('/')
def index():
    return render_template('index.html', title='Home')


@main_page.route('/<string:username>/home')
@login_required
def home(username):
    page = request.args.get('page', 1, type=int)
    print("Page number= ", page)

    posts = Post.query.order_by(Post.publish_date.desc()).paginate(page=page, per_page=5)
    form = Posts()
    return render_template('home.html', posts=posts, title="Home")


@main_page.route('/about')
def about():
    return render_template('about.html', title="About")
