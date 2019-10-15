from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flaskblog.config import Config




# Database initialization
db = SQLAlchemy()
# Encryption Initilization
bcrypt = Bcrypt()
# Login Manager Initialization
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message = 'You have to login to access this page!'
login_manager.login_message_category = 'info'
#Configuring email server
mail = Mail()




def create_app(config = Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from flaskblog.main.routes import main_page
    from flaskblog.users.routes import users
    from flaskblog.posts.routes import posts
    from flaskblog.errors.handlers import errors
    app.register_blueprint(main_page)
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(errors)

    return app