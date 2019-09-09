from flask import Blueprint, Flask, jsonify, request, Response
from flask_pymongo import PyMongo
import os
from dotenv import load_dotenv
import json
import bcrypt
from flask_cors import CORS, cross_origin
import datetime
from bson.json_util import ObjectId
import jwt
import cloudinary as Cloud
from cloudinary import uploader
print(datetime.datetime.now())


load_dotenv()

app = Flask(__name__)
app.config['MONGO_DBNAME'] = os.getenv('MONGO_DBNAME')
app.config['MONGO_URI'] = os.getenv('MONGO_URI')
# connect(os.getenv('MONGO_DBNAME'), host=os.getenv('MONGO_URI'), port=11968, username='mansoor', password='mansoor11', retryWrites=False)
Cloud.config.update = ({
    'cloud_name':os.getenv('CLOUDINARY_CLOUD_NAME'),
    'api_key': os.getenv('CLOUDINARY_API_KEY'),
    'api_secret': os.getenv('CLOUDINARY_API_SECRET')
})

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
# "image_id": "dsudhuf",
# "video_id": "dsuhuis"
# "createdBy": "Mansoor",
# "user_id": "dfsudhir",
# "slug": ["user_id", "heading", "author", "timestamps"],
# }


@article_blueprint.route("/")
def index():
    api = mongo.db.article.find_one({'_id': ObjectId('5d6e715fce7b8f762204dc41') })
    encoded = jwt.encode({'some': 'payload'}, 'secretToken', algorithm='HS256')
    pipeshelf = uploader.upload("v1.mp4", resource_type = "video", chunk_size = 1000000000)
    encoded = str(encoded).split("'")
    print(pipeshelf)
    return jsonify({ "message" : "Wellcome To RESTFUL APIs Articles", "secretToken": encoded, "url": pipeshelf })


@article_blueprint.route("/add", methods=["POST"])
def add():
    article = mongo.db.article
    images = mongo.db.images
    videos = mongo.db.videos
    data = request.form
    fileData = request.files
    print(mongo.db.list_collection_names())
    print(data)
    print(fileData['image'])
    image_upload = uploader.upload(fileData['image'])
    image_result = {
        "image": image_upload,
        "image_desc": data['image_desc'],
        "timestamp": datetime.datetime.now()
    }
    if(fileData['video']):
        video_upload = uploader.upload(fileData['video'], resource_type = "video", chunk_size = 1000000000)
        video_result = {
            "video": video_upload,
            "video_desc": data['video_']
        }
    # print(mongo.db.dropDatabase())
    # result = article.insert_one(data)
    # print('result', result.inserted_id)
    return jsonify({ 'success': True, 'message': 'Successfully Registered', 'resulted_id': 'str(result.inserted_id)' })


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
        "depublishing": "sgsgysy",
        "user_id": "dfsudhir"
    })
    print(result.inserted_id)
    return jsonify({ 'success': True, 'message': 'Successfully Registered', 'resulted_id': str(result.inserted_id)})


@article_blueprint.route("/gallery", methods=["POST"])
def gallery():
    gallery = mongo.db.gallery
    data = request.get_json(force=True)
    result = gallery.insert_one({
        "name": "abc",
        "imageIds": [],
        "slug": "dsuhirtuyuighiuy",
        "user_id": "dfsudhir"
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
        "depublishing": "sgsgysy",
        "user_id": "dfsudhir"
    })
    print(result.inserted_id)
    return jsonify({ 'success': True, 'message': 'Successfully Registered', 'resulted_id': str(result.inserted_id)})



@article_blueprint.route("/category", methods=["POST"])
def category():
    category = mongo.db.category
    data = request.get_json(force=True)
    result = category.insert_one({
       "name": "abc",
       "slug": ["user_id", "heading", "author", "timestamps"]
    })
    print(result.inserted_id)
    return jsonify({ 'success': True, 'message': 'Successfully Registered', 'resulted_id': str(result.inserted_id)})


@article_blueprint.route("/topic", methods=["POST"])
def topic():
    topic = mongo.db.topic
    data = request.get_json(force=True)
    result = topic.insert_one({
       "name": "abc",
       "description": "fhjgfgjhgefj",
       "slug": ["user_id", "heading", "author", "timestamps"]
    })
    print(result.inserted_id)
    return jsonify({ 'success': True, 'message': 'Successfully Registered', 'resulted_id': str(result.inserted_id)})


@article_blueprint.route("/city", methods=["POST"])
def city():
    city = mongo.db.city
    data = request.get_json(force=True)
    result = city.insert_one({
       "name": "abc",
       "slug": ["user_id", "heading", "author", "timestamps"]
    })
    print(result.inserted_id)
    return jsonify({ 'success': True, 'message': 'Successfully Registered', 'resulted_id': str(result.inserted_id)})