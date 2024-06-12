#!/usr/bin/python3
"""
    place views
"""
from flask import jsonify, abort, request
from AirBnB_clone_v2.models import review
from models.place import Place
from api.v1.views import app_views
from models import storage
from models.review import Review


@app_views.route('places/<places_id>/reviews',
                 strict_slashes=False, methods=['GET'])
def get_place_of_place(places_id):
    """ 
        Retrieves all place of a Place
        object
    """
    all_place = []
    place_obj = storage.get(Place, str(places_id))

    if place_obj is None:
        abort(404)

    for place in place_obj.places:
        all_place.append(place.to_dict())

    return jsonify(all_place)


@app_views.route('/reviews/<review_id>', strict_slashes=False, methods=['GET'])
def get_place_id(review_id):
    """
        Retrives place by its ID
    """
    fetch_id = storage.get(Review, str(review_id))

    if fetch_id is None:
        abort(404)

    return jsonify(fetch_id.to_json())


@app_views.route('/reviews/<review_id>', strict_slashes=False, methods=['GET', 'DELETE'])
def del_place(review_id):
    """
        This delete a place object
    """
    fetch_id = storage.get(Place, str(review_id))
    if fetch_id is None:
        abort(404)

    storage.delete(fetch_id)
    storage.save()

    return jsonify({}), 200


@app_views.route('/places/<places_id>/reviews', strict_slashes=False, methods=['POST'])
def create_place(place_id):
    """
        This create a new instance of place
    """
    review_json = request.get_json()

    fetch_Place = storage.get(place_id)
    if fetch_Place is None:
        abort(404)

    if review_json is None:
        abort(400, 'Not a JSON')

    if "user_id" not in review_json:
        abort(400, 'Missing user_id')

    if "text" not in review_json:
        abort(400, 'Missing text')

    review_json["place_id"] = place_id

    obj = Review(**review_json)
    storage.new(obj)
    storage.save()

    return jsonify(obj.to_dict()), 200


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['PUT'])
def update_place(review_id):
    fetch_obj = storage.get(Review, str(review_id))
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
