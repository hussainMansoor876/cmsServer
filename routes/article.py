from flask import Blueprint, Flask, jsonify, request, Response
from flask_pymongo import PyMongo
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv
import json
import bcrypt
from flask_cors import CORS, cross_origin
import datetime
from bson.json_util import ObjectId
# print(datetime.datetime.now())


load_dotenv()

app = Flask(__name__)
app.config['MONGO_DBNAME'] = os.getenv('MONGO_DBNAME')
app.config['MONGO_URI'] = os.getenv('MONGO_URI')
# connect(os.getenv('MONGO_DBNAME'), host=os.getenv('MONGO_URI'), port=11968, username='mansoor', password='mansoor11', retryWrites=False)


# class Article(Document):
#     email = StringField(required=True)
#     first_name = StringField(required=True)
#     password = ListField(max_length=50)


article_blueprint = Blueprint('article', __name__)
mongo = PyMongo(app, retryWrites=False, connect= True )

# {
# "heading":"abc",
# "subheadline": "abc123",
# "text": "lorem ipsum",
# "author": "Mansoor",
# "city": "Karachi",
# "categories": ["deded"],
# "topics": ["abc","dfsd"],
# "gNews": ["da","asd","edd","rdf","rzsrt"],
# "mark": true,
# "future_time": "43678",
# "de_time": 7846874,
# "timestamp": 9048094,
# "last_modified": 37467,
# "createdBy": "Mansoor"
# }


@article_blueprint.route("/")
def index():
    api = mongo.db.article.find_one({'_id': ObjectId('5d6e715fce7b8f762204dc41') })
    print(api)
    return jsonify({ "message" : "Wellcome To RESTFUL APIs Articles" })


@article_blueprint.route("/add", methods=["POST"])
def add():
    article = mongo.db.article
    data = request.get_json(force=True)
    print(mongo.db.list_collection_names())
    print(mongo.db.dropDatabase())
    result = article.insert_one(data)
    print('result', result.inserted_id)
    return jsonify({ 'success': True, 'message': 'Successfully Registered', 'resulted_id': str(result.inserted_id)})


@article_blueprint.route("/images", methods=["POST"])
def image():
    image = mongo.db.image
    data = request.get_json(force=True)
    result = image.insert_one({
        "filename": "abc",
        "copyright": "Mansoor",
        "description": "nfjknjkdfkjf",
        "keywords": "jfhdfukd",
        "symbol": True,
        "free": True,
        "timestamps": datetime.datetime.now(),
        "uploaded": "user",
        "depublishing": "sgsgysy"
    })
    print(result.inserted_id)
    return jsonify({ 'success': True, 'message': 'Successfully Registered', 'resulted_id': str(result.inserted_id)})


@article_blueprint.route("/gallery", methods=["POST"])
def gallery():
    gallery = mongo.db.gallery
    data = request.get_json(force=True)
    result = gallery.insert_one({
        "name": "abc",
        "imageIds": []
    })
    print(result.inserted_id)
    return jsonify({ 'success': True, 'message': 'Successfully Registered', 'resulted_id': str(result.inserted_id)})


@article_blueprint.route("/video", methods=["POST"])
def video():
    video = mongo.db.video
    data = request.get_json(force=True)
    result = video.insert_one({
       "filename": "abc",
        "copyright": "Mansoor",
        "headline": "fydgyudfguygvyuxgfy",
        "description": "nfjknjkdfkjf",
        "keywords": "jfhdfukd",
        "preview": "yfr",
        "free": True,
        "timestamps": datetime.datetime.now(),
        "uploaded": "user",
        "depublishing": "sgsgysy"
    })
    print(result.inserted_id)
    return jsonify({ 'success': True, 'message': 'Successfully Registered', 'resulted_id': str(result.inserted_id)})



@article_blueprint.route("/category", methods=["POST"])
def category():
    category = mongo.db.category
    data = request.get_json(force=True)
    result = category.insert_one({
       "name": "abc",
    })
    print(result.inserted_id)
    return jsonify({ 'success': True, 'message': 'Successfully Registered', 'resulted_id': str(result.inserted_id)})