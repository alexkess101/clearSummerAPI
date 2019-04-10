from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_heroku import Heroku
from flask_bcrypt import Bcrypt
from datetime import datetime
from statistics import mean


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
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=True)
    current_sales = db.Column(db.Integer, nullable=False)
    num_sales_goal = db.Column(db.Integer, nullable=False)
    income_current = db.Column(db.Integer, nullable=False)
    income_total = db.Column(db.Integer, nullable=False)
    commission_percentage = db.Column(db.Float, nullable=False)
    expenseHistory = db.relationship('ExpenseHistory', backref='user', lazy=True)
    saleHistory = db.relationship('SaleHistory', backref='user', lazy=True)
    incentiveHistory = db.relationship('IncentiveHistory', backref='user', lazy=True)

    def __init__(self, email, password, start_date, end_date, current_sales, num_sales_goal, income_current, income_total, commission_percentage):
        self.email = email
        self.password = password
        self.start_date = start_date
        self.end_date = end_date
        self.current_sales = current_sales
        self.num_sales_goal = num_sales_goal
        self.income_current = income_current
        self.income_total = income_total
        self.commission_percentage = commission_percentage
        
        

    def __repr__(self):
        return '<Title %r>' % self.title


class ExpenseHistory(db.Model):
    __tablename__="expenseHistory"
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, server_default=db.func.now())
    expense = db.Column(db.String(250), nullable=False)
    expense_amount = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, date_created, expense, expense_amount, user_id):
        self.date_created = date_created
        self.expense = expense
        self.expense_amount == expense_amount
        self.user_id = user_id

class SaleHistory(db.Model):
    __tablename__="saleHistory"
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, server_default=db.func.now())
    account_name_first = db.Column(db.String(150), nullable=False)
    account_name_last = db.Column(db.String(150), nullable=False)
    account_value = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, account_name_first, account_name_last, account_value, user_id):
        self.account_name_first = account_name_first
        self.account_name_last = account_name_last
        self.account_value = account_value
        self.user_id = user_id

class IncentiveHistory(db.Model):
    __tablename__='incentiveHistory'
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, server_default=db.func.now())
    incentive_name = db.Column(db.String(150), nullable=False)
    incentive_value = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, date_created, incentive_name, incentive_value, user_id):
        self.date_created = date_created
        self.incentive_name = incentive_name
        self.incentive_value = incentive_value
        self.user_id = user_id





@app.route('/')
def home():
    return "<h1>Jchillin</h1>"

@app.route('/all_users', methods=['GET'])
def get_all_users():
    verified_user = db.session.query(User.id, User.email, User.password, User.start_date, User.end_date, User.commission_percentage).all()
    return jsonify(verified_user)

@app.route('/new_user', methods=['POST'])
def User_input():
    if request.content_type == 'application/json':
        post_data = request.get_json()
        email = post_data.get('email')
        password = post_data.get('password')
        start_date = post_data.get('start_date')
        end_date = post_data.get('end_date')
        current_sales = post_data.get('current_sales')
        num_sales_goal = post_data.get('num_sales_goal')
        income_current = post_data.get('income_current')
        income_total = post_data.get('income_total')
        commission_percentage = post_data.get('commission_percentage')
    
        user = User(email, password, start_date, end_date, current_sales, num_sales_goal, income_current, income_total, commission_percentage)
        db.session.add(user)
        db.session.commit()

        new_user = db.session.query(User.id, User.email, User.password).filter(User.email == email).all()
        return jsonify(new_user)
    return jsonify("Something went wrong with adding a user")



@app.route('/login', methods=['POST'])
def get_users():
    post_data = request.get_json()
    post_email = post_data.get('email')
    post_password = post_data.get('password')
    verified_user = db.session.query(User.id, User.email, User.password).filter(User.email == post_email).all()
    
    return jsonify(verified_user)

@app.route('/user/delete/<id>', methods=['DELETE'])
def delete_user(id):
    user = db.session.query(User).get(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify("User deleted")


@app.route('/home/<id>/create_sale', methods=['POST'])
def post_sale(id):
    if request.content_type == 'application/json':
        post_data = request.get_json()
        account_name_first = post_data.get('account_name_first')
        account_name_last = post_data.get('account_name_last')
        account_value = post_data.get('account_value')
        user = db.session.query(User).get(id)
        
        add_income = account_value * user.commission_percentage
        current_sales = db.session.query(User).get(id)
        current_sales.income_current = current_sales.income_current + add_income

        reg = SaleHistory(account_name_first, account_name_last, account_value, id)
        db.session.add(reg)
        db.session.commit()
        return jsonify("Everything has worked correctly")
    return jsonify("Something went wrong with adding a sale")

@app.route('/sale/<id>/view_sales', methods=['GET'])
def get_sale(id):
    sale = db.session.query(SaleHistory.id, SaleHistory.date_created, SaleHistory.account_name_first, SaleHistory.account_name_last, SaleHistory.account_value).filter(SaleHistory.user_id==id).order_by(SaleHistory.date_created.desc()).all()
    return jsonify(sale)


@app.route('/sale', methods=['GET'])
def get_all_sale():
    sale = db.session.query(SaleHistory.id, SaleHistory.date_created, SaleHistory.account_name_first, SaleHistory.account_name_last, SaleHistory.account_value, SaleHistory.user_id).all()
    return jsonify(sale)

@app.route('/home/<id>', methods=['GET'])
def get_user_info(id):
    total_income_goal = db.session.query(User.income_total).filter(User.id == id).first()
    income_current = db.session.query(User.income_current).filter(User.id == id).first()
    num_sales_goal = db.session.query(User.num_sales_goal).filter(User.id == id).first()
    num_sales = db.session.query(SaleHistory).filter(SaleHistory.user_id == id).count()
    user_commission_value = db.session.query(User.commission_percentage).filter(User.id == id).first()
    value_sales = db.session.query(SaleHistory.account_value).filter(SaleHistory.user_id ==id).all()
    

    return jsonify(total_income_goal, income_current, num_sales_goal, num_sales, value_sales, user_commission_value)





        


if __name__ == "__main__":
    app.debug = True
    app.run()







