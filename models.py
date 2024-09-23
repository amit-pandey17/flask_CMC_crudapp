# models.py
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum as SQLAEnum
from enums import UserRole

db = SQLAlchemy()

class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    role = db.Column(SQLAEnum(UserRole), nullable=False)

    def __init__(self, name, email, role):
        self.name = name
        self.email = email
        self.role = role