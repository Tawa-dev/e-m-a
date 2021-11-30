from re import I
from flask import Flask

app = Flask(__name__)

from app import views
from app import veld_view
from app import defore_view
from app import main_views
from app import litter_view
from app.database import Database


@app.before_first_request
def initialize_database():
    Database.initialize()
