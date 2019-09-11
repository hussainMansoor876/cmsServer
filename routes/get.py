from flask import Blueprint, Flask, jsonify, request, Response
from flask_pymongo import PyMongo
import os
from dotenv import load_dotenv
import json
import bcrypt
import jwt
from flask_cors import CORS, cross_origin
from bson.json_util import ObjectId
import cloudinary as Cloud
from cloudinary import uploader

load_dotenv()

app = Flask(__name__)
app.config['MONGO_DBNAME'] = os.getenv('MONGO_DBNAME')
app.config['MONGO_URI'] = os.getenv('MONGO_URI')


get_blueprint = Blueprint('get', __name__)
mongo = PyMongo(app, retryWrites=False)

Cloud.config.update = ({
    'cloud_name':os.getenv('CLOUDINARY_CLOUD_NAME'),
    'api_key': os.getenv('CLOUDINARY_API_KEY'),
    'api_secret': os.getenv('CLOUDINARY_API_SECRET')
})


@get_blueprint.route("/article/<id>")
def articleGet(id):
    article = mongo.db.article
    article_data = article.find({"uid": id})
    data = []
    for x in article_data:
        x['_id'] = str(x['_id'])
        data.append(x)
    return jsonify({'success': False, 'message': 'Invalid Email Or Password!!!', "data": data})

