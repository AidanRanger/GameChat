from flask import Flask, g, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login.mixins import UserMixin
from flask_login.utils import login_required, logout_user
from flask_login import LoginManager, login_user, current_user
from datetime import datetime

###########################################################################################################
#initialization
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager(app)
###########################################################################################################
#classes
class user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable = False) 
    password = db.Column(db.String(50), nullable = False)
    def __repr__(self):
        return f'Username: {self.username}'
    def check_password(self, password):
        return self.password == password

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
###########################################################################################################
#routes
@app.route('/')
def home():
     return render_template('home.html')

@app.route('/login', methods=['GET','POST'])
def login():
    return render_template('login.html')
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form.get('username')).first()
        if user and user.check_password(request.form.get('password')): 
            login_user(user)
            return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)