from flask import Flask,\
render_template, url_for, \
redirect, request, session, redirect, jsonify
from flask_pymongo import PyMongo
from routes.login import index_blueprint
from flask_cors import CORS

app = Flask(__name__)

app.register_blueprint(index_blueprint, url_prefix='/login')

CORS(app)



@app.route("/")
def index():
    return jsonify({"name": "Mansoor"})


if __name__=="__main__":
    app.run(debug=True)