#!/usr/bin/python3
"""
The RESTful api starts here. The api aids data access in the app.
"""
from os import getenv

from flask import Flask, jsonify
from flask_cors import CORS

from api.v1.views import app_views
from models import storage

app = Flask(__name__)

app.register_blueprint(app_views)
CORS(app,  resources={r"/*": {"origins": "0.0.0.0"}})

host = getenv("HBNB_API_HOST", "0.0.0.0")
port = getenv("HBNB_API_PORT", "5000")


@app.teardown_appcontext
def teardown(exception):
    """Cleanup operations"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Print Error"""
    data = {"error": "Not found"}
    response = jsonify(data)
    response.status_code = 404


if __name__ == "__main__":
    app.run(host, port, threaded=True, debug=True)
