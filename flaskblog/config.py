import secrets
import os


class Config:
    FLASK_APP = "run.py"
    SECRET_KEY = secrets.token_hex(26)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///blog.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BCRYPT_LOG_ROUND = 16
    BCRYPT_HANDLE_LONG_PASSWORDS = True
    MAIL_PORT = 587
    MAIL_USE_SSL = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
