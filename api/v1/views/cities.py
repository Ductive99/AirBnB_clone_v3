#!/usr/bin/python3
"""City view"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def get_state_cities(state_id):
    """Retrieves the list of all City objects of a State."""
    state_objs = storage.get(State, state_id)
    if not state_objs:
        abort(404)
    return jsonify([city.to_dict() for city in state_objs.cities])


@app_views.route('/cities/<city_id>', methods=['GET'])
def get_city(city_id):
    """Retrieves a City object."""
    obj = storage.get(City, city_id)
    if not obj:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE', 'PUT'])
def UD_city(city_id):
    """Updates or Deletes a City object"""
    obj = storage.get(City, city_id)
    if not obj:
        abort(404)

    if request.method == "DELETE":
        obj.delete()
        storage.save()
        return jsonify({})

    info = request.get_json(silent=True)
    if not info:
        abort(400, "Not a JSON")
    for k, v in info.items():
        if k not in ['id', 'created_at', 'updated_at', 'state_id']:
            setattr(obj, k, v)
    obj.save()
    return jsonify(obj.to_dict())


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def create_city(state_id):
    """Creates a City."""
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    info = request.get_json(silent=True)
    if not info:
        abort(400, "Not a JSON")
    if 'name' not in info:
        abort(400, "Missing name")

    obj = City(**info)
    setattr(obj, 'state_id', state_id)
    storage.new(obj)
    storage.save()
    return jsonify(obj.to_dict()), 201
