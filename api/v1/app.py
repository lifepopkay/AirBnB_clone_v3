#!/usr/bin/python3
"""
Script that imports a 
Blueprint and runs Flask
listining to port
0.0.0.0
"""

from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)

app.register_blueprint(app_views)

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
