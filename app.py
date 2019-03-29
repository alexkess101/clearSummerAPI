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
    __tablename__="user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    num_sales_goal = db.Column(db.Integer, nullable=False)
    income_total = db.Column(db.Integer, nullable=False)
    commission_percentage = db.Column(db.Float, nullable=False)
    signing_bonuses = db.Column(db.Integer, nullable=True)
    incentives = db.Column(db.Integer, nullable=True)
    expenses = db.Column(db.Integer, nullable=True)
    

    def __init__(self, email, password, num_sales_goal, income_total, commission_percentage, signing_bonuses, incentives, expenses):
        self.email = email
        self.password = password
        self.num_sales_goal = num_sales_goal
        self.income_total = income_total
        self.commission_percentage = commission_percentage
        self.signing_bonuses = signing_bonuses
        self.incentives = incentives
        self.expenses = expenses

    def __repr__(self):
        return '<Title %r>' % self.title






@app.route('/')
def home():
    return "<h1>Jchillin</h1>"

@app.route('/user/new', methods=['POST'])
def User_input():
    if request.content_type == 'application/json':
        post_data = request.get_json()
        email = post_data.get('email')
        password = post_data.get('password')
        

        commission_percentage = post_data.get('commission_percentage')
        signing_bonuses = post_data.get('signing_bonuses')
        incentives = post_data.get('incentives')

        num_sales_goal = post_data.get('num_sales_goal')
        income_total = post_data.get('income_total')

        user = User(email, password)

        db.session.add(user)
        db.session.commit()
        return jsonify("Everything has worked correctly")
    return jsonify("Something went wrong with adding a user")


@app.route('/login', methods=['GET'])
def get_users():
    users = db.session.query(User.id, User.email, User.password).all()
    return jsonify(users)

@app.route('/user/delete/<id>', methods=['DELETE'])
def delete_user(id):
    user = db.session.query(User).get(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify("User deleted")


        


if __name__ == "__main__":
    app.debug = True
    app.run()







