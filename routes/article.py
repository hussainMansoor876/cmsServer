from flask import Blueprint, Flask, jsonify, request, Response
from flask_pymongo import PyMongo
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv
import json
import bcrypt
from flask_cors import CORS, cross_origin


load_dotenv()

app = Flask(__name__)
app.config['MONGO_DBNAME'] = os.getenv('MONGO_DBNAME')
app.config['MONGO_URI'] = os.getenv('MONGO_URI')


article_blueprint = Blueprint('article', __name__)
mongo = PyMongo(app, retryWrites=False)


@article_blueprint.route("/")
def signin():
    return jsonify({ "message" : "Wellcome To RESTFUL APIs Articles" })

