# Flask CRUD CMC app

This is a Flask web application that uses SQLAlchemy for database management. The following instructions will help you set up and run this project on your local machine.
Listens to port: http://127.0.0.1:5000

## Table of Contents

- [Getting Started](#getting-started)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Built With](#built-with)
- [Authors](#authors)
- [License](#license)

## Getting Started

These instructions will guide you through setting up and running the project on your local machine for development and testing purposes.

## Prerequisites

Before you begin, ensure you have the following installed:

- [Python 3.9.6](https://www.python.org/downloads/release/python-396/)
- [pip](https://pip.pypa.io/en/stable/installation/)
- [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

## Installation

1. **Clone the Repository**:

    ```sh
    git clone https://github.com/<USERNAME>/<REPO>.git
    cd <REPO>
    ```

2. **Create a Virtual Environment**:

    ```sh
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install Dependencies**:

    ```sh
    pip install -r requirements.txt
    ```

4. **Set Up Environment Variables**:

    Create a `.env` file in the project root and add any necessary environment variables (e.g., database URL, secret keys).

    Example `.env` file:
    ```sh
    FLASK_APP=run.py
    FLASK_ENV=development
    SQLALCHEMY_DATABASE_URI=sqlite:///site.db
    SECRET_KEY=your_secret_key_here
    ```

5. **Initialize the Database**:

    ```sh
    flask db init
    flask db migrate -m "Initial migration."
    flask db upgrade
    ```

## Running the Application

To run the application, use the following command:

```sh
flask run
```

Visit [http://127.0.0.1:5000](http://127.0.0.1:5000) in your web browser to see the application in action.

## Built With

- [Flask](https://flask.palletsprojects.com/) - Micro web framework for Python
- [SQLAlchemy](https://www.sqlalchemy.org/) - SQL toolkit and Object-Relational Mapping (ORM) library for Python
- [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/) - Integration of SQLAlchemy with Flask
- [Flask-Migrate](https://flask-migrate.readthedocs.io/) - Handles SQLAlchemy database migrations for Flask applications using Alembic
- [Flask-Paginate](https://pythonhosted.org/Flask-paginate/) - Pagination support for Flask applications

## Authors

- **Amit Pandey**

## License

TBD
