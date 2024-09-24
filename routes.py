# routes.py
import re
from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Data
from sqlalchemy.exc import SQLAlchemyError
from enums import UserRole
import logging
from config import Config

logger = Config.logger
main = Blueprint('main', __name__)

# Regex patterns for validation
NAME_REGEX = r'^[A-Za-z0-9\s]+$'  # Allows alphabetic characters and spaces
EMAIL_REGEX = r'^[\w\.-]+@[\w\.-]+\.\w+$'  # Basic email format validation


@main.route('/')
def index():
    # Pagination parameters
    page = request.args.get('page', 1, type=int)
    per_page = 5  # Number of records per page

    # Querying data with pagination
    all_data = Data.query.paginate(page=page, per_page=per_page)

    return render_template('index.html', users=all_data)
@main.route('/insert', methods=['POST'])
def insert():
    try:
        if request.method == 'POST':
            name = request.form['name']
            email = request.form['email']
            role = request.form['role']

            # Validate name
            if not re.match(NAME_REGEX, name):
                flash("Error: Invalid name. Only alphabetic characters are allowed.")
                return redirect(url_for('main.index'))

            # Validate email
            if not re.match(EMAIL_REGEX, email):
                flash("Error:Invalid email format.")
                return redirect(url_for('main.index'))

            # Check if role is a valid UserRole
            if role in UserRole.__members__:
                role = UserRole[role]
            else:
                flash("Error:Invalid user role.")
                return redirect(url_for('main.index'))

            # Create a new Data object
            my_data = Data(name=name, email=email, role=role)

            # Add and commit to the database
            db.session.add(my_data)
            db.session.commit()

            logger.info(f"Insertion successful: {my_data}")
            flash("User inserted successfully!")
            return redirect(url_for('main.index'))

    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Database transaction failed - /insert: {e}")
        flash("Failed to insert user. Please try again.")
        return redirect(url_for('main.index'))

    except Exception as e:
        logger.error(f"An unexpected error occurred - /insert: {e}")
        flash("An unexpected error occurred. Please try again.")
        return redirect(url_for('main.index'))

@main.route('/update', methods=['POST'])
def update():
    try:
        if request.method == 'POST':
            my_data = Data.query.get(request.form.get('id'))
            if not my_data:
                flash("User not found!")
                return redirect(url_for('main.index'))

            name = request.form['name']
            email = request.form['email']
            role = request.form['role']

            # Validate name
            if not re.match(NAME_REGEX, name):
                flash("Error:Invalid name. Only alphabetic characters are allowed.")
                return redirect(url_for('main.index'))

            # Validate email
            if not re.match(EMAIL_REGEX, email):
                flash("Error:Invalid email format.")
                return redirect(url_for('main.index'))

            # Update user data
            my_data.name = name
            my_data.email = email

            # Check if role is a valid UserRole
            if role in UserRole.__members__:
                my_data.role = UserRole[role]
            else:
                flash("Error:Invalid user role.")
                return redirect(url_for('main.index'))

            db.session.commit()
            logger.info(f"Update successful: {my_data}")

            flash("User updated successfully!")
            return redirect(url_for('main.index'))

    except SQLAlchemyError as e:
        db.session.rollback()

        logger.error(f"Database transaction failed - /update: {e}")
        flash("Failed to update user. Please try again.")
        return redirect(url_for('main.index'))

    except Exception as e:
        logger.error(f"An unexpected error occurred - /update: {e}")
        flash("An unexpected error occurred. Please try again.")
        return redirect(url_for('main.index'))

@main.route('/delete/<id>', methods=['POST'])
def delete(id):
    try:
        my_data = Data.query.get(id)
        if not my_data:
            flash("User not found!")
            return redirect(url_for('main.index'))

        db.session.delete(my_data)
        db.session.commit()

        logger.info("Deleted successfully")
        flash("User deleted successfully!")
        return redirect(url_for('main.index'))

    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Database transaction failed - /delete: {e}")
        return redirect(url_for('main.index'))