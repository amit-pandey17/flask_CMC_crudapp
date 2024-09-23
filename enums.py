# enums.py
from enum import Enum

class UserRole(Enum):
    Admin = "Admin"
    Staff = "Staff"
    Student = "Student"
    Guest = "Guest"