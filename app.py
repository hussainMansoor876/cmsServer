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

app.register_blueprint(index_blueprint, url_prefix='/login')
# app.config['MONGO_DBNAME'] = os.getenv('MONGO_DBNAME')
# app.config['MONGO_URI'] = os.getenv('MONGO_URI')
# mongo = PyMongo(app, retryWrites=False)

CORS(app, origins=["http://localhost:3000", "https://quiz-assignment-8e887.firebaseapp.com/"], allow_headers=[
        "Content-Type", "Authorization", "Access-Control-Allow-Credentials"],
        supports_credentials=True)

@app.route('/', methods=["POST"])
def index():
    return 'Wellcome To RESTFUL APIs'




if __name__=="__main__":
    app.run(debug=True)