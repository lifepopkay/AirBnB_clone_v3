#!/usr/bin/python3
"""
The RESTful api starts here. The api aids data access in the app.
"""
from models import storage
from api.v1.views import app_views

from flask import Flask, jsonify
from flask_cors import CORS
from os import getenv


app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

app.register_blueprint(app_views)

host = getenv("HBNB_API_HOST", "0.0.0.0")
port = getenv("HBNB_API_PORT", "5000")


@app.teardown_appcontext
def teardown(exception):
  """Cleanup operations"""
  storage.close()

@app.errorhandler(404)
def not_found(error):
  data = {"error": "Not found"}
  res =  jsonify(data)
  res.status_code = 404
  return(res)


if __name__ == "__main__":
  app.run(host, port, threaded=True, debug=True)
