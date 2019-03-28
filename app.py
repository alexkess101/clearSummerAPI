from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_heroku import Heroku


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)
SQLALCHEMY_TRACK_MODIFICATIONS = False
#Don't know what this error is all about

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    goals = db.relationship('Goals', backref='User', lazy=True)
    income = db.relationship('Income', backref='User', lazy=True)
    expenses = db.relationship('Expenses', backref='User', lazy=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username


class Goals(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    num_sales_goal = db.Column(db.Integer, nullable=False)
    income_total = db.Column(db.Integer, nullable=False)
    User_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)

    def __init__(self, num_sales_goal, income_total):
        self.num_sales_goal = num_sales_goal
        self.income_total = income_total


class Income(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    commission_percentage = db.Column(db.Integer, nullable=False)
    signing_bonuses = db.Column(db.Integer, nullable=True)
    incentives = db.Column(db.Integer, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Expenses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rent = db.Column(db.Integer, nullable=True)
    other_expenses = db.Column(db.Integer, nullable=True)


@app.route('/')
def home():
    return "<h1>Jchillin</h1>"







