from flask import Flask, g, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
'''
from flask_login.mixins import UserMixin
from flask_login.utils import login_required, logout_user
from flask_login import LoginManager, login_user, current_user
from wtforms import Form, BooleanField, StringField, PasswordField, validators
'''
from datetime import datetime
import sqlite3
###########################################################################################################
#initialization
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
DATABASE = './DATABASES/db.sqlite3'
###########################################################################################################
UserGames = db.Table('UserGames',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('games_id', db.Integer, db.ForeignKey('games.id'), primary_key=True)
)
class Publisher(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String)

class Games(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    publisher_id = db.Column(db.Integer, ForeignKey('publisher.id'))

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True) 
    
#functions

def get_db():
    db = getattr(g,'_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

#routes
@app.route('/')
def home():
    return render_template('home.html')

'''
@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    #if form.validate_on_submit():
    #    login_user(user)
    #    flask.flash('Login Successful')
    return render_template('login.html', form=form)

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
'''
@app.route('/Add')
def Add():
    return render_template('NewData.html')

@app.route('/Info')
def Info():
    return render_template('Info.html')

@app.route('/games')
def games():
    cursor = get_db().cursor()
    sql = 'SELECT games.csgo, games.LoL, games.Apex, games.CoD FROM  JOIN games ON .games_id=games.id JOIN user ON .user_id=user.id'
    cursor.execute(sql)
    results = cursor.fetchall()
    return render_template('games.html', results=results)

@app.route('/GameTable')
def GameTable():
    cursor = get_db().cursor()
    sql = 'SELECT user.username, games.csgo, games.LoL, games.Apex, games.CoD FROM  JOIN games ON .games_id=games.id JOIN user ON .user_id=user.id'
    cursor.execute(sql)
    results = cursor.fetchall()
    return render_template('Game-Table.html', results=results )

if __name__ == "__main__":
    app.run(debug=True)