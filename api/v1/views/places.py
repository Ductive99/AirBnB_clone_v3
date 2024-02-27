#!/usr/bin/python3
"""Places view"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.city import City
from models.user import User
from models.place import Place


@app_views.route('/cities/<city_id>/places', methods=['GET'])
def get_city_places(city_id):
    """Retrieves the list of all Place objects of a City."""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify([place.to_dict() for place in city.places])


@app_views.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    """Retrieves a Place object."""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """Deletes a Place object."""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def create_place(city_id):
    """Creates a Place."""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    info = request.get_json(silent=True)
    if not info:
        abort(400, "Not a JSON")
    if 'user_id' not in info:
        abort(400, "Missing user_id")
    if 'name' not in info:
        abort(400, "Missing name")

    user_id = info['user_id']
    if storage.get(User, user_id) is None:
        abort(404)
    info['city_id'] = city_id
    place = Place(**info)
    storage.new(place)
    storage.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    """Updates a Place object."""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    info = request.get_json(silent=True)
    if not info:
        abort(400, "Not a JSON")

    for key, value in info.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200
