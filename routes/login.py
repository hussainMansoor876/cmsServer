from flask import Blueprint, Flask
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'cms-frontend'
app.config['MONGO_URI'] = 'mongodb://mansoor:mansoor11@ds311968.mlab.com:11968/cms-frontend'
mongo = PyMongo(app)

print(mongo)

index_blueprint = Blueprint('login', __name__)



@index_blueprint.route('/')
def loginUser():
    return "Hello"