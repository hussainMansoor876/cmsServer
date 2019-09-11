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
    return jsonify({"data": data})


@get_blueprint.route("/article/all")
def articleGetAll():
    article = mongo.db.article
    article_data = article.find({})
    data = []
    for x in article_data:
        x['_id'] = str(x['_id'])
        data.append(x)
    return jsonify({"data": data})


@get_blueprint.route("/images/<id>")
def imageGet(id):
    image = mongo.db.image
    gallery = mongo.db.gallery
    data = request.form
    fileData = request.files
    image_upload = uploader.upload(fileData['image'])
    gallery_result = gallery.find_one({"name": data['gallery_name']})
    if gallery_result:
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
            "gallery_name": data['gallery_name'],
            "gallery_id": str(gallery_result['_id'])
        }
        image_result = image.insert_one(image_data)
        gallery_result['image_id'].append(str(image_result.inserted_id))
        gallery.find_one_and_update({"name": data['gallery_name']}, {
                                    "$set": {"image_id": gallery_result['image_id']}})
    else:
        gallery_new = {
            "name": data['gallery_name'],
            "image_id": []
        }
        gallery_result = gallery.insert_one(gallery_new)
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
            "gallery_name": data['gallery_name'],
            "gallery_id": str(gallery_result.inserted_id)
        }
        image_result = image.insert_one(image_data)
        gallery_new['image_id'].append(str(image_result.inserted_id))
        gallery.find_one_and_update({"name": data['gallery_name']}, {
                                    "$set": {"image_id": gallery_new['image_id']}})

    return jsonify({'success': True, 'message': 'Successfully Uploaded'})


@get_blueprint.route("/gallery")
def gallery():
    gallery = mongo.db.gallery
    data = request.form
    gallery_data = {
        "name": data['name'],
        "image_id": []
    }
    gallery.insert_one(gallery_data)
    return jsonify({'success': True, 'message': 'Successfully Added Gallery'})


@get_blueprint.route("/video")
def video():
    video = mongo.db.video
    data = request.form
    fileData = request.files

    image_upload = uploader.upload(fileData['prev_image'])
    video_upload = uploader.upload(
        fileData['video'], resource_type="video", chunk_size=1000000000)
    video_data = {
        "copyright": data['copyright'],
        "headline": data['headline'],
        "video_desc": data['video_desc'],
        "prev_image": image_upload,
        "video": video_upload,
        "free": data['free'],
        "timestamps": datetime.datetime.now(),
        "userName": data['userName'],
        "depublishing": data['depublishing'],
        "uid": data['uid']
    }
    video.insert_one(video_data)
    return jsonify({'success': True, 'message': 'Successfully Uploaded'})


@get_blueprint.route("/category")
def category():
    category = mongo.db.category
    data = request.form
    category.insert_one({
        "name": data['name']
    })
    return jsonify({'success': True, 'message': 'Successfully Added'})


@get_blueprint.route("/topic")
def topic():
    topic = mongo.db.topic
    data = request.form
    topic.insert_one({
        "name": data['name'],
        "description": data['description']
    })
    return jsonify({'success': True, 'message': 'Successfully Registered'})


@get_blueprint.route("/city")
def city():
    city = mongo.db.city
    data = request.form
    city.insert_one({
        "name": data['name']
    })
    return jsonify({'success': True, 'message': 'Successfully Registered'})
