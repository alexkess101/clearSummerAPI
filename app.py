from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_heroku import Heroku
from flask_bcrypt import Bcrypt


app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgres://tqyqpoohjfrpcs:60abb1bb09a6dc0905a17ea24244b6b7883d43ff5b9a7b9165b3a3f92c00a1d9@ec2-174-129-10-235.compute-1.amazonaws.com:5432/ddbugnvvbd1n5e'

heroku = Heroku(app)
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=True, nullable=False)
    goals = db.relationship('Goals', backref='User', lazy=True)
    income = db.relationship('Income', backref='User', lazy=True)
    expenses = db.relationship('Expenses', backref='User', lazy=True)

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def __repr__(self):
        return '<Title %r>' % self.title

class Goals(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    num_sales_goal = db.Column(db.Integer, nullable=False)
    income_total = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)

    def __init__(self, num_sales_goal, income_total, user_id):
        self.num_sales_goal = num_sales_goal
        self.income_total = income_total
        self.user_id = user_id


class Income(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    commission_percentage = db.Column(db.Integer, nullable=False)
    signing_bonuses = db.Column(db.Integer, nullable=True)
    incentives = db.Column(db.Integer, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)

    def __init__(self, commission_percentage, incentives, user_id):
        self.commission_percentage = commission_percentage
        self.incentives = incentives
        self.user_id = user_id

class Expenses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rent = db.Column(db.Integer, nullable=True)
    other_expenses = db.Column(db.Integer, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)

    def __init__(self, rent, other_expenses, user_id):
        self.rent = rent
        self.other_expenses = other_expenses
        self.user_id = user_id


@app.route('/')
def home():
    return "<h1>Jchillin</h1>"

@app.route('/user/input', methods=['POST'])
def User_input():
    if request.content_type == 'application/json':
        post_data = request.get_json()
        email = post_data.get('email')
        password = post_data.get('password')

        reg = User(email, password)
        db.session.add(reg)
        db.session.commit()
        return jsonify("User Added")
    return jsonify("Something went wrong with adding a user")

@app.route('/users', methods=['GET'])
def get_users():
    users = db.session.query(User.email, User.password).all()
    return jsonify(users)
        


if __name__ == "__main__":
    app.debug = True
    app.run()







