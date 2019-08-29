from flask import Flask,\
render_template, url_for, \
redirect, request, session, jsonify
from flask_pymongo import PyMongo
from dotenv import load_dotenv
import bcrypt
import os


load_dotenv()

from flask_cors import CORS, cross_origin
from routes.login import index_blueprint

app = Flask(__name__)

# app.register_blueprint(index_blueprint, url_prefix='/login')
app.config['MONGO_DBNAME'] = os.getenv('MONGO_DBNAME')
app.config['MONGO_URI'] = os.getenv('MONGO_URI')
mongo = PyMongo(app, retryWrites=False)

cors = CORS(app)


@app.route("/", methods=["POST"])
def index():
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

@app.route("/register", methods=["POST"])
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



if __name__=="__main__":
    app.run(debug=True)