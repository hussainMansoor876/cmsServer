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
def galleryGet():
    gallery = mongo.db.gallery
    return jsonify({'success': True, 'message': 'Successfully Added Gallery'})


# @get_blueprint.route("/video")
# def videoGet():
#     video = mongo.db.video
#     return jsonify({'success': True, 'message': 'Successfully Uploaded'})


# @get_blueprint.route("/category")
# def categoryGet():
#     category = mongo.db.category
#     return jsonify({'success': True, 'message': 'Successfully Added'})


# @get_blueprint.route("/topic")
# def topicGet():
#     topic = mongo.db.topic
#     return jsonify({'success': True, 'message': 'Successfully Registered'})


# @get_blueprint.route("/city")
# def cityGet():
#     city = mongo.db.city
#     return jsonify({'success': True, 'message': 'Successfully Registered'})
