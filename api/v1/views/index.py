#!/usr/bin/python3
"""Initialize flask functions"""
from flask import jsonify, make_response
from api.v1.views import app_views
from models import storage

classes = {"Amenity": "amenities", "City": "cities",
           "Place": "places", "Review": "reviews",
           "State": "states",
           "User": "users"}


@app_views.route('/status',
                 methods=['GET'], strict_slashes=False)
def view_status():
    """Returns a JSON"""
    response = jsonify({"status": "OK"})
    response.headers["Content-Type"] = "application/json"
    response.status_code = 200
    return response


@app_views.route('/stats',
                 methods=['GET'], strict_slashes=False)
def storage_stats():
    """Returns a JSON"""
    dict_count = {}
    for key, val in classes.items():
        dict_count[val] = storage.count(key)

    return jsonify(dict_count)
