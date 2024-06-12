#!/usr/bin/python3
"""
    City views
"""
from flask import jsonify, abort, request
from models.state import State
from api.v1.views import app_views
from models import storage
from models.city import City


@app_views.route('states/<state_id>/cities',
                 strict_slashes=False, methods=['GET'])
def get_city_by_State(state_id):
  """
    Retrieves all city of a state
    object
  """
  all_city = []
  state_obj = storage.get(State, str(state_id))

  if state_obj is None:
    abort(404)

  for city in state_obj.cities:
    all_city.append(city.to_dict())

  return jsonify(all_city)


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['GET'])
def get_City_id(city_id):
  """
    Retrives City by its ID
  """
  fetch_id = storage.get(City, str(city_id))

  if fetch_id is None:
    abort(404)

  return jsonify(fetch_id.to_json())


@app_views.route('/cities/<city_id>', strict_slashes=False,
                 methods=['GET', 'DELETE'])
def del_City(City_id):
  """
    This delete a City object
  """
  fetch_id = storage.get(City, str(City_id))
  if fetch_id is None:
    abort(404)

  storage.delete(fetch_id)
  storage.save()

  return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', strict_slashes=False,
                 methods=['POST'])
def create_City(state_id):
  """
    This create a new instance of City
  """
  City_json = request.get_json()
  fetch_state = storage.get(state_id)
  if fetch_state is None:
    abort(404)

  if City_json is None:
    abort(400, 'Not a JSON')

  if "name" not in City_json:
    abort(400, 'Missing name')

  City_json["state_id"] = state_id

  obj = City(**City_json)
  storage.new(obj)
  storage.save()

  return jsonify(obj.to_dict()), 200


@app_views.route('/Citys/<City_id>', strict_slashes=False,
                 methods=['PUT'])
def update_City(City_id):
  fetch_obj = storage.get(City, str(City_id))
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
