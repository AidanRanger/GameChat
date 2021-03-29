from flask import Flask, g, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
#db.init_app(app)

class user(db.Model):
    id = db.column(db.integer, primary_key=True)
    username = db.column(db.String(20), nullable = False) 
    password = db.column(db.String(20), nullable = False)