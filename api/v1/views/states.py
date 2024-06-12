#!/usr/bin/python3
"""
  state views
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', strict_slashes=False, methods=['GET'])
def get_state():
    """
     Retrives all states objects
    """
    all_state = []
    state_in_storage = storage.all(State)
    for obj in state_in_storage.values():
        all_state.append(obj.to_json())

    return jsonify(all_state)


@app_views.route('/states/<state_id>',
                 strict_slashes=False, methods=['GET'])
def get_state_id(state_id):
    """
     Retrives state by its ID
    """
    fetch_id = storage.get(State, str(state_id))

    if fetch_id is None:
        abort(404)

    return jsonify(fetch_id.to_json())


@app_views.route('/states/<state_id>',
                 strict_slashes=False, methods=['GET', 'DELETE'])
def del_state(state_id):
    """
     This delete a state object
    """
    fetch_id = storage.get(State, str(state_id))
    if fetch_id is None:
        abort(404)

    storage.delete(fetch_id)
    storage.save()

    return jsonify({}), 200


@app_views.route('/states',
                 strict_slashes=False, methods=['POST'])
def create_state():
    """
     This create a new instance of state
    """
    state_json = request.get_json()
    if state_json is None:
        abort(400, 'Not a JSON')

    if "name" not in state_json:
        abort(400, 'Missing name')

    obj = State(**state_json)
    storage.new(obj)
    storage.save()

    return jsonify(obj.to_dict()), 200


@app_views.route('/states/<state_id>',
                 strict_slashes=False,
                 methods=['PUT'])
def update_state(state_id):
    fetch_obj = storage.get(State, str(state_id))
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
