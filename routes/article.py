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
import datetime
from slugify import slugify
# print(datetime.date.today())
# print(datetime.datetime.now())
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

# print(mongo.db.list_collection_names())
# print(mongo.db.image)


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
    data = dict(data)
    fileData = request.files
    slug = slugify(data['headline'])
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
    arrData = {
        'city': json.loads(data['city']),
        'author': json.loads(data['author']),
        'categories': json.loads(data['categories']),
        'topics': json.loads(data['topics']),
        'gNews': json.loads(data['gNews']),
    }
    for key, value in arrData.items():
        for i, val in enumerate(value):
            arrData[key][i] = val.title()
    article_data = {
        "headline": data['headline'],
        "subheadline": data['subheadline'],
        "text": data['text'],
        "author": arrData['author'],
        "city": arrData['city'],
        "categories": arrData['categories'],
        "topics": arrData['topics'],
        "gNews": arrData['gNews'],
        "free": data['free'],
        "publishing": datetime.datetime.strptime(data['publishing'], "%Y-%m-%d %H:%M:%S"),
        "depublishing": datetime.datetime.strptime(data['depublishing'], "%Y-%m-%d %H:%M:%S"),
        "timestamp": datetime.datetime.now(),
        "last_modified": datetime.datetime.now(),
        "imageData": image_result,
        "videoData": video_result,
        "createdBy": data['userName'],
        "uid": data['uid'],
        "slug": slug,
        "status": 'published'
    }
    article_added = article.insert_one(article_data)
    slug = str(article_added.inserted_id)+"/"+slug
    article.find_one_and_update({"_id": article_added.inserted_id}, {
                                "$set": {"slug": slug}})
    return jsonify({'success': True, 'message': 'Successfully Registered'})


@article_blueprint.route("/image", methods=["POST"])
def image():
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
        slug = slugify(data['gallery_name'])
        gallery_new = {
            "name": data['gallery_name'],
            "image_id": [],
            "uid": data['uid'],
            "slug": slug
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
        slug = str(gallery_result.inserted_id)+"/"+slug
        gallery.find_one_and_update({"_id": gallery_result.inserted_id}, {
                                    "$set": {"slug": slug}})
        image_result = image.insert_one(image_data)
        gallery_new['image_id'].append(str(image_result.inserted_id))
        gallery.find_one_and_update({"name": data['gallery_name']}, {
                                    "$set": {"image_id": gallery_new['image_id']}})

    return jsonify({'success': True, 'message': 'Successfully Uploaded'})


@article_blueprint.route("/gallery", methods=["POST"])
def gallery():
    gallery = mongo.db.gallery
    data = request.form
    slug = slugify(data['name'])
    gallery_data = {
        "name": data['name'],
        "uid": data['uid'],
        "slug": slug,
        "image_id": []
    }
    gallery_added = gallery.insert_one(gallery_data)
    slug = str(gallery_added.inserted_id)+"/"+slug
    gallery.find_one_and_update({"_id": gallery_added.inserted_id}, {
                                "$set": {"slug": slug}})
    return jsonify({'success': True, 'message': 'Successfully Added Gallery'})


@article_blueprint.route("/video", methods=["POST"])
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


@article_blueprint.route("/category", methods=["POST"])
def category():
    category = mongo.db.category
    data = request.form
    slug = slugify(data['name'])
    category_added = category.insert_one({
        "name": data['name'],
        "slug": slug
    })
    slug = str(category_added.inserted_id)+"/"+slug
    category.find_one_and_update({"_id": category_added.inserted_id}, {
                                 "$set": {"slug": slug}})
    return jsonify({'success': True, 'message': 'Successfully Added'})


@article_blueprint.route("/topic", methods=["POST"])
def topic():
    topic = mongo.db.topic
    data = request.form
    slug = slugify(data['name'])
    topic_added = topic.insert_one({
        "name": data['name'],
        "description": data['description']
    })
    slug = str(topic_added.inserted_id)+"/"+slug
    topic.find_one_and_update({"_id": topic_added.inserted_id}, {
                              "$set": {"slug": slug}})
    return jsonify({'success': True, 'message': 'Successfully Registered'})


@article_blueprint.route("/city", methods=["POST"])
def city():
    city = mongo.db.city
    data = request.form
    slug = slugify(data['name'])
    city_data = city.find_one({"name": data['name'].title()})
    if city_data:
        return jsonify({'success': False, 'message': 'Already city added'})
    city_added = city.insert_one({
        "name": data['name'].title()
    })
    slug = str(city_added.inserted_id)+"/"+slug
    city.find_one_and_update({"_id": city_added.inserted_id}, {
                             "$set": {"slug": slug}})
    return jsonify({'success': True, 'message': 'Successfully Registered'})
