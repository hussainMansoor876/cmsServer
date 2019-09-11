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
    'cloud_name': os.getenv('CLOUDINARY_CLOUD_NAME'),
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
    return jsonify({'data': data})


@get_blueprint.route("/article/all")
def articleGetAll():
    article = mongo.db.article
    article_data = article.find({})
    data = []
    for x in article_data:
        x['_id'] = str(x['_id'])
        data.append(x)
    return jsonify({'data': data})


@get_blueprint.route("/image/<id>")
def imageGet(id):
    image = mongo.db.image
    image_data = image.find({"uid": id})
    data = []
    for x in image_data:
        x['_id'] = str(x['_id'])
        data.append(x)
    return jsonify({'data': data})

@get_blueprint.route("/image/all")
def imageGetAll():
    image = mongo.db.image
    image_data = image.find({})
    data = []
    for x in image_data:
        x['_id'] = str(x['_id'])
        data.append(x)
    return jsonify({'data': data})


@get_blueprint.route("/gallery/<id>")
def galleryGet(id):
    gallery = mongo.db.gallery
    gallery_data = gallery.find({"uid": id})
    data = []
    for x in gallery_data:
        x['_id'] = str(x['_id'])
        data.append(x)
    return jsonify({'data': data})

@get_blueprint.route("/gallery/all")
def galleryGetAll():
    gallery = mongo.db.gallery
    image = mongo.db.image
    gallery_data = gallery.find({})
    data = []
    for x in gallery_data:
        x['_id'] = str(x['_id'])
        for i, v in enumerate(x['image_id']):
            image_data = image.find_one({'_id': ObjectId(v)})
            image_data['_id'] = str(image_data['_id'])
            x['image_id'][i] = image_data
        data.append(x)
    return jsonify({'data': data})


@get_blueprint.route("/video/<id>")
def videoGet(id):
    video = mongo.db.video
    video_data = video.find({"uid": id})
    data = []
    for x in video_data:
        x['_id'] = str(x['_id'])
        data.append(x)
    return jsonify({'data': data})

@get_blueprint.route("/video/all")
def videoGetAll():
    video = mongo.db.video
    video_data = video.find({})
    data = []
    for x in video_data:
        x['_id'] = str(x['_id'])
        data.append(x)
    return jsonify({'data': data})


@get_blueprint.route("/category/all")
def categoryGet():
    category = mongo.db.category
    category_data = category.find({})
    data = []
    for x in category_data:
        x['_id'] = str(x['_id'])
        data.append(x)
    return jsonify({'data': data})


@get_blueprint.route("/topic/all")
def topicGet():
    topic = mongo.db.topic
    topic_data = topic.find({})
    data = []
    for x in topic_data:
        x['_id'] = str(x['_id'])
        data.append(x)
    return jsonify({'data': data})


@get_blueprint.route("/city/all")
def cityGet():
    city = mongo.db.city
    city_data = city.find({})
    data = []
    for x in city_data:
        x['_id'] = str(x['_id'])
        data.append(x)
    return jsonify({'data': data})
