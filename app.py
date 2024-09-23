from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum as SQLAEnum  # Avoid name conflict with Python's enum

# DB credentials: un: root@localhost, pw:Password123

app = Flask(__name__)
app.secret_key = "Secret!"

# Use PyMySQL as the MySQL driver
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Password123@localhost/crud_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # disable warning

db = SQLAlchemy(app)

# Define Enum for roles
from enum import Enum


class UserRole(Enum):
    Admin = "Admin"
    Staff = "Staff"
    Student = "Student"
    Guest = "Guest"


class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    role = db.Column(SQLAEnum(UserRole), nullable=False)  # Enum for role

    def __init__(self, name, email, role):
        self.name = name
        self.email = email
        self.role = role


@app.route('/')
def index():  # put application's code here
    return render_template('index.html')


@app.route('/insert', methods=['POST'])
def insert():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        role = UserRole[request.form['role']]  # Convert to UserRole enum

        my_data = Data(name, email, role)  # Data object
        db.session.add(my_data)
        db.session.commit()

        flash("User inserted successfully!")

        return redirect(url_for('index', msg='Data Inserted'))


if __name__ == '__main__':
    db.create_all()  # Create tables if they don't exist
    app.run(debug=True)  # change this later on for prod
