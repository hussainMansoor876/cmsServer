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
# print(datetime.datetime.now())
# print(mongo.db.list_collection_names())
# print('result', result.inserted_id)


load_dotenv()

app = Flask(__name__)
app.config['MONGO_DBNAME'] = os.getenv('MONGO_DBNAME')
app.config['MONGO_URI'] = os.getenv('MONGO_URI')

Cloud.config.update = ({
    'cloud_name': os.getenv('CLOUDINARY_CLOUD_NAME'),
    'api_key': os.getenv('CLOUDINARY_API_KEY'),
    'api_secret': os.getenv('CLOUDINARY_API_SECRET')
})


article_blueprint = Blueprint('article', __name__)
mongo = PyMongo(app, retryWrites=False, connect=True)



@article_blueprint.route("/")
def index():
    api = mongo.db.article.find_one(
        {'_id': ObjectId('5d6e715fce7b8f762204dc41')})
    encoded = jwt.encode({'some': 'payload'}, 'secretToken', algorithm='HS256')
    pipeshelf = uploader.upload(
        "v1.mp4", resource_type="video", chunk_size=1000000000)
    encoded = str(encoded).split("'")
    print(pipeshelf)
    return jsonify({"message": "Wellcome To RESTFUL APIs Articles", "secretToken": encoded, "url": pipeshelf})


@article_blueprint.route("/add", methods=["POST"])
def add():
    article = mongo.db.article

    data = request.form
    fileData = request.files

    image_upload = uploader.upload(fileData['image'])
    image_result = {
        "image": image_upload,
        "image_desc": data['image_desc'],
        "timestamp": datetime.datetime.now()
    }
    video_result = {}
    if('video' in fileData):
        video_upload = uploader.upload(
            fileData['video'], resource_type="video", chunk_size=1000000000)
        video_result = {
            "video": video_upload,
            "video_desc": data['video_desc'] if 'video_desc' in data else None,
            "timestamp": datetime.datetime.now()
        }
    article_data = {
        "heading": data['heading'],
        "subheadline": data['subheadline'],
        "text": data['text'],
        "author": data['author'],
        "city": data['city'],
        "categories": data['categories'],
        "topics": data['topics'],
        "gNews": data['gNews'],
        "mark": data['mark'],
        "publishing": data['publishing'],
        "depublishing": data['depublishing'],
        "timestamp": datetime.datetime.now(),
        "last_modified": data['last_modified'],
        "imageData": image_result,
        "videoData": video_result,
        "createdBy": data['userName'],
        "user_id": data['uid'],
        "slug": data['slug'],
        "status": data['status']
    }
    article_added = article.insert_one(article_data)
    print(article_added.inserted_id)
    return jsonify({'success': True, 'message': 'Successfully Registered' })


@article_blueprint.route("/images", methods=["POST"])
def image():
    image = mongo.db.image
    data = request.form
    fileData = request.files
    image_upload = uploader.upload(fileData['image'])
    image_data = {
        "copyright": data['copyright'],
        "imageData": image_upload,
        "image_desc": data['image_desc'],
        "userName": data['userName'],
        "uid": data['uid'],
        "free": data['free'],
        "symbol_image": data['symbol_image'],
        "timestamp": datetime.datetime.now(),
        "depublishing": data['depublishing'],
        "gallery_id": data['gallery_id']
    }
    image.insert_one(image_data)
    return jsonify({'success': True, 'message': 'Successfully Uploaded'})


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
    return jsonify({'success': True, 'message': 'Successfully Registered', 'resulted_id': str(result.inserted_id)})


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
    return jsonify({'success': True, 'message': 'Successfully Registered', 'resulted_id': str(result.inserted_id)})


@article_blueprint.route("/category", methods=["POST"])
def category():
    category = mongo.db.category
    data = request.form
    result = category.insert_one({
        "name": data['name']
    })
    print(result.inserted_id)
    return jsonify({'success': True, 'message': 'Successfully Registered'})


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
    return jsonify({'success': True, 'message': 'Successfully Registered', 'resulted_id': str(result.inserted_id)})


@article_blueprint.route("/city", methods=["POST"])
def city():
    city = mongo.db.city
    data = request.get_json(force=True)
    result = city.insert_one({
        "name": "abc",
        "slug": ["user_id", "heading", "author", "timestamps"]
    })
    print(result.inserted_id)
    return jsonify({'success': True, 'message': 'Successfully Registered', 'resulted_id': str(result.inserted_id)})
