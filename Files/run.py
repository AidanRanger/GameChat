from flask import Flask, g, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login.mixins import UserMixin
from flask_login.utils import login_required, logout_user
from flask_login import LoginManager, login_user, current_user
from datetime import datetime
import sqlite3
###########################################################################################################
#initialization
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
DATABASE = './DATABASES/db.sqlite3'
###########################################################################################################
#classes
usergames = db.Table('usergames',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('games_id', db.Integer, db.ForeignKey('games.id'), primary_key=True)
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True) 
    password = db.Column(db.String(50), nullable=False)
    def __repr__(self):
        return f'Username: {self.username}'
    def check_password(self, password):
        return self.password == password

class Games(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    csgo = db.Column(db.String, nullable=False)
    LoL = db.Column(db.String, nullable=False)
    Apex = db.Column(db.String, nullable=False)
    CoD = db.Column(db.String, nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
###########################################################################################################
#Logins
login_manager.login_view = "users.login"
###########################################################################################################
#functions

def get_db():
    db = getattr(g,'_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

###########################################################################################################
#routes
@app.route('/')
def home():
     return render_template('home.html')

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        login_user(user)
    flask.flash('Login Successful')
@app.route('/signup')
def signup():
    if request.method == "POST":
        cursor = get_db().cursor()
        newuser = request.form['username']

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return 'You are now logged out!'

    return render_template('signup.html')
@app.route('/games')

def games():
    cursor = get_db().cursor()
    sql = 'SELECT csgo FROM games'
    cursor.execute(sql)
    csgo = cursor.fetchall()
    sql = 'SELECT Lol FROM games'
    cursor.execute(sql)
    LoL = cursor.fetchall()
    sql = 'SELECT Apex FROM games'
    cursor.execute(sql)
    Apex = cursor.fetchall()
    sql = 'SELECT CoD FROM games'
    cursor.execute(sql)
    CoD = cursor.fetchall()
    return render_template('games.html', csgo = csgo, LoL = LoL, Apex = Apex, CoD = CoD)


if __name__ == "__main__":
    app.run(debug=True)