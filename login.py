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


index_blueprint = Blueprint('login', __name__)
mongo = PyMongo(app, retryWrites=False)

CORS(index_blueprint, origins=["http://localhost:3000", "https://quiz-assignment-8e887.firebaseapp.com/"], allow_headers=[
        "Content-Type", "Authorization", "Access-Control-Allow-Credentials"],
        supports_credentials=True)


@index_blueprint.route('/', methods=["POST"])
@cross_origin(headers=['Content-Type'])
def loginUser():
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
        output = []
        for s in add.find():
            output.append({'name': s['name'], 'email': s['email'],
                        'password': s['password'], '_id': str(s['_id'])})
        return jsonify({'result': output})


@index_blueprint.route('/register', methods=["POST"])
def registerUser():
    add = mongo.db.user
    data = request.get_json(force=True)
    existUser = add.find_one({'email': data['email']})
    if(existUser):
        return jsonify({'success': False, 'message': 'User Already Exist!!!'})
    else:
        hashed_password = bcrypt.hashpw(data['password'].encode('utf8'), bcrypt.gensalt(12))
        add.insert_one({'name': data['name'], 'email': data['email'], 'password': hashed_password})
        return jsonify({ 'success': True, 'message': 'Successfully Registered'})
