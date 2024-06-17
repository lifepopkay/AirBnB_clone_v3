#!/usr/bin/python3
"""
  Amenity views
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', strict_slashes=False,
                 methods=['GET'])
def get_Amenity():
    """
     Retrives all amenities objects
    """
    all_Amenity = []
    Amenity_in_storage = storage.all(Amenity)
    for obj in Amenity_in_storage.values():
        all_Amenity.append(obj.to_json())

    return jsonify(all_Amenity)


@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False, methods=['GET'])
def get_amenity_id(amenity_id):
    """
     Retrives Amenity by its ID
    """
    fetch_id = storage.get(Amenity, str(amenity_id))

    if fetch_id is None:
        abort(404)

    return jsonify(fetch_id.to_json())


@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False, methods=['GET', 'DELETE'])
def del_Amenity(amenity_id):
    """
     This delete a Amenity object
    """
    fetch_id = storage.get(Amenity, str(amenity_id))
    if fetch_id is None:
        abort(404)

    storage.delete(fetch_id)
    storage.save()

    return jsonify({}), 200


@app_views.route('/amenities',
                 strict_slashes=False,
                 methods=['POST'])
def create_Amenity():
    """
     This create a new instance of Amenity
    """
    Amenity_json = request.get_json()
    if Amenity_json is None:
        abort(400, 'Not a JSON')

    if "name" not in Amenity_json:
        abort(400, 'Missing name')

    obj = Amenity(**Amenity_json)
    storage.new(obj)
    storage.save()

    return jsonify(obj.to_dict()), 200


@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False,
                 methods=['PUT'])
def update_Amenity(amenity_id):
    fetch_obj = storage.get(Amenity, str(amenity_id))
    if fetch_obj is None:
        abort(404)

    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')

    for key, val in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(fetch_obj, key, val)

    storage.save()
    return jsonify(fetch_obj.to_dict()), 200
