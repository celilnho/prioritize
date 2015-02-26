from . import db 
from werkzeug import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin, current_user
from . import login_manager 
from datetime import datetime

@login_manager.user_loader 
def load_user(user_id):
    if user_id == None or user_id == 'None':
        user_id = -1
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(100), unique = True)
    password_hash = db.Column(db.String(200))


    def __init__(self, u, p):
        self.username = u
        self.set_password(p)

    def __str__(self):
        return "<Username %s>" %(self.username)

    @property 
    def password(self):
        raise AttributeError("password is not a readable attr")

    def set_password(self,p):
        self.password_hash = generate_password_hash(p)

    def check_password(self, formPassword):
        return check_password_hash(self.password_hash, formPassword)

    # functions for Flask-Login

    def is_authenticated(self):
        return True 

    def is_active(self):
        return True 

    def is_anonymous(self):
        return False 

    def get_id(self):
        return unicode(self.id)

    @classmethod
    def get_username(cls, u):
        return cls.query.filter_by(username = u).first()




