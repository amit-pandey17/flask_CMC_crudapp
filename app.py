from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "Secret!"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/crud_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #disable warning

db = SQLAlchemy(app)



@app.route('/')
def index():  # put application's code here
    return render_template('index.html')

class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    role = db.Column(db.String(100)) # TO do: Enum

    def __init__(self, name, email, role):
        self.name = name
        self.email = email
        self.role = role


if __name__ == '__main__':
    app.run(debug = True) #change this later on for prod
