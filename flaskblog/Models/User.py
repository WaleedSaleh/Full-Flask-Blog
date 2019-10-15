from datetime import datetime
from flask import current_app
from flaskblog import db, bcrypt, login_manager
from flask_login import UserMixin
from itsdangerous import JSONWebSignatureSerializer as Serializer, TimestampSigner


# here we'll create our login_loader in order to load the user id from the session

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    image_file = db.Column(db.String(60), nullable=True, default='default.jpg')
    creation_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    posts = db.relationship('Post', backref='author', lazy=True)


    def reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], )
        return s.dumps({"user_id": self.id}).decode('utf-8')

    @staticmethod
    def verify_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}' , '{self.email}', '{self.image_file}')"

    def setHashedPassword(self, password):
        self.password = bcrypt.generate_password_hash(password=password).decode('utf-8')

    def checkHashedPassword(self, password):
        return bcrypt.check_password_hash(self.password, password=password)
