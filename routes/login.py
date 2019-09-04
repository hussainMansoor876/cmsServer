from flask import Blueprint, Flask, jsonify, request, Response
from flask_pymongo import PyMongo
import os
from dotenv import load_dotenv
import json
import bcrypt
import jwt
from flask_cors import CORS, cross_origin


load_dotenv()

app = Flask(__name__)
app.config['MONGO_DBNAME'] = os.getenv('MONGO_DBNAME')
app.config['MONGO_URI'] = os.getenv('MONGO_URI')


index_blueprint = Blueprint('login', __name__)
mongo = PyMongo(app, retryWrites=False)


@index_blueprint.route("/signin", methods=["POST"])
def signin():
    add = mongo.db.user
    data = request.get_json(force=True)
    existUser = add.find_one({'email': data['email']})
    if(existUser):
        passwordCheck=bcrypt.checkpw(data['password'].encode('utf8'), existUser['password'])
        if(passwordCheck):
            return jsonify({'success': True, 'message': 'User Find!!!'})
        else:
            return jsonify({'success': False, 'message': 'Invalid Email Or Password!!!'})
    else:
        return jsonify({'success': False, 'message': 'Invalid Email Or Password!!!'})



@index_blueprint.route("/register", methods=["POST"])
def registerUser():
    add = mongo.db.user
    data = request.get_json(force=True)
    existUser = add.find_one({'email': data['email']})
    if(existUser):
        return jsonify({'success': False, 'message': 'User Already Exist!!!'})
    else:
        # hashed_password = bcrypt.hashpw(data['password'].encode('utf8'), bcrypt.gensalt(12))
        encoded = jwt.encode(data, 'secretToken', algorithm='HS256')
        encoded = str(encoded).split("'")
        # add.insert_one({ 
        #     'name': data['name'], 
        #     'email': data['email'], 
        #     'password': hashed_password,
        #     'avatar': data['avatar'],
        #     'secretToken': 'secret',
        #     'role': 'Admin'
        #     })
        return jsonify({ 'success': True, 'message': 'Successfully Registered', "secretToken": encoded })
