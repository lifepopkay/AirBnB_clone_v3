#!/usr/bin/python3
"""
    user views
"""
from re import U
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', strict_slashes=False, methods=['GET'])
def get_user():
    """
        Retrives all users objects
    """
    all_user = []
    user_in_storage = storage.all(User)
    for obj in user_in_storage.values():
        all_user.append(obj.to_json())

    return jsonify(all_user)


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['GET'])
def get_user_id(user_id):
    """
        Retrives user by its ID
    """
    fetch_id = storage.get(User, str(user_id))

    if fetch_id is None:
        abort(404)

    return jsonify(fetch_id.to_json())


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['GET', 'DELETE'])
def del_user(user_id):
    """
        This delete a user object
    """
    fetch_id = storage.get(User, str(user_id))
    if fetch_id is None:
        abort(404)

    storage.delete(fetch_id)
    storage.save()

    return jsonify({}), 200


@app_views.route('/users', strict_slashes=False, methods=['POST'])
def create_user():
    """
        This create a new instance of user
    """
    user_json = request.get_json()
    if user_json is None:
        abort(400, 'Not a JSON')

    if "email" not in user_json:
        abort(400, 'Missing email')

    if "password" not in user_json:
        abort(400, 'Missing password')

    obj = User(**user_json)
    storage.new(obj)
    storage.save()

    return jsonify(obj.to_dict()), 200


@app_views.route('/users/<user_id>', strict_slashes=False,
                 methods=['PUT'])
def update_user(user_id):
    fetch_obj = storage.get(User, str(user_id))
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
