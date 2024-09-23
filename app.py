import logging
from http.cookiejar import debug

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum as SQLAEnum  # Avoid name conflict with Python's enum
from sqlalchemy.exc import SQLAlchemyError  # For catching SQLAlchemy errors
import logging

# DB credentials: un: root@localhost, pw:Password123

logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


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

    def __init__(self, name, email, role, dob):
        self.name = name
        self.email = email
        self.role = role


@app.route('/')
def index():  # put application's code here
    all_data = Data.query.all()
    return render_template('index.html', users=all_data)


@app.route('/insert', methods=['POST'])
def insert():
    try:
        if request.method == 'POST':
            name = request.form['name']
            email = request.form['email']
            role = UserRole[request.form['role']]  # Convert to UserRole enum
            my_data = Data(name, email, role)  # Data object

            db.session.add(my_data)
            db.session.commit()

            #logging - success
            logger.info(f"insertion successful: {my_data}")

            flash("User inserted successfully!")
            return redirect(url_for('index'))

    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Database transaction failed - /Insert: {e}")  # Log the error
        return redirect(url_for('index'))


@app.route('/update', methods=['POST'])
def update():
    try:
        if request.method == 'POST':
            my_data = Data.query.get(request.form.get('id'))
            if not my_data:
                flash("User not found!")
                return redirect(url_for('index'))

            my_data.name = request.form['name']
            my_data.email = request.form['email']
            my_data.role = UserRole[request.form['role']]

            db.session.commit()
            logger.info(f"Update successful: {my_data}")

            flash("User updated successfully!")
            return redirect(url_for('index'))

    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Database transaction failed - /Update: {e}")
        return redirect(url_for('index'))


@app.route('/delete/<id>', methods=['POST'])
def delete(id):
    try:
        my_data = Data.query.get(id)
        if not my_data:
            flash("User not found!")
            return redirect(url_for('index'))

        db.session.delete(my_data)
        db.session.commit()

        logger.info("Deleted successfully")

        flash("User deleted successfully!")
        return redirect(url_for('index'))

    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Database transaction failed - /Delete: {e}")
        return redirect(url_for('index'))


if __name__ == '__main__':
    db.create_all()  # Create tables if they don't exist (with each deployment)
    app.run(debug=True)  # change this later on for prod