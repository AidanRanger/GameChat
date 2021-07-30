from flask import Flask, g, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login.mixins import UserMixin
from flask_login.utils import login_required, logout_user
from flask_login import LoginManager, login_user, current_user
from wtforms import Form, BooleanField, StringField, PasswordField, validators
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
    apex = db.Column(db.String, nullable=False)
    CoD = db.Column(db.String, nullable=False)
  
class LoginForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('New Password', [
        validators.DataRequired()
    ])

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
    return flask.render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(form.username.data, form.password.data)
        db_session.add(user)
        flash('Thanks for registering')
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return 'You are now logged out!'

    return render_template('signup.html')
@app.route('/games')

def games():
    cursor = get_db().cursor()
    sql = 'SELECT games.csgo, games.LoL, games.Apex, games.CoD FROM usergames JOIN games ON usergames.games_id=games.id JOIN user ON usergames.user_id=user.id'
    cursor.execute(sql)
    results = cursor.fetchall()
    return render_template('games.html', results=results)

@app.route('/GameTable')

def GameTable():
    cursor = get_db().cursor()
    sql = 'SELECT user.username, games.csgo, games.LoL, games.Apex, games.CoD FROM usergames JOIN games ON usergames.games_id=games.id JOIN user ON usergames.user_id=user.id'
    cursor.execute(sql)
    results = cursor.fetchall()
    return render_template('Game-Table.html', results=results )
if __name__ == "__main__":
    app.run(debug=True)