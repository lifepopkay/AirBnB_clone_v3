#!/usr/bin/python3
"""
    City views
"""
from flask import jsonify, abort, request
from models.place import Place
from api.v1.views import app_views
from models import storage
from models.city import City


@app_views.route('cities/<city_id>/places',
                 strict_slashes=False, methods=['GET'])
def get_place_of_city(city_id):
    """
        Retrieves all city of a Place
        object
    """
    all_place = []
    city_obj = storage.get(City, str(city_id))

    if city_obj is None:
        abort(404)

    for place in city_obj.places:
        all_place.append(city.to_dict())

    return jsonify(all_place)


@app_views.route('/places/<place_id>', strict_slashes=False, methods=['GET'])
def get_place_id(place_id):
    """
        Retrives City by its ID
    """
    fetch_id = storage.get(Place, str(place_id))

    if fetch_id is None:
        abort(404)

    return jsonify(fetch_id.to_json())


@app_views.route('/places/<place_id>',
                 strict_slashes=False, methods=['GET', 'DELETE'])
def del_place(place_id):
    """
        This delete a City object
    """
    fetch_id = storage.get(Place, str(place_id))
    if fetch_id is None:
        abort(404)

    storage.delete(fetch_id)
    storage.save()

    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places',
                 strict_slashes=False, methods=['POST'])
def create_place(place_id):
    """
        This create a new instance of City
    """
    place_json = request.get_json()

    fetch_Place = storage.get(place_id)
    if fetch_Place is None:
        abort(404)

    if place_json is None:
        abort(400, 'Not a JSON')

    if "user_id" not in place_json:
        abort(400, 'Missing user_id')

    if "name" not in place_json:
        abort(400, 'Missing name')

    place_json["place_id"] = place_id

    obj = City(**place_json)
    storage.new(obj)
    storage.save()

    return jsonify(obj.to_dict()), 200


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['PUT'])
def update_place(place_id):
    fetch_obj = storage.get(Place, str(place_id))
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
