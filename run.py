from app import app
from db import db

# required because of how uwsgi starts the app
# app.py is not directly called
db.init_app(app)


@app.before_first_request
def create_tables():
    db.create_all()
