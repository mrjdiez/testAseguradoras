from functools import wraps

from server.models import User
from server import utils

from sqlalchemy.exc import IntegrityError
from flask import Blueprint, request, make_response, g, jsonify, abort
from sqlalchemy import select
from werkzeug.exceptions import HTTPException

user_bp = Blueprint('user', __name__)


@user_bp.route('/', methods=['POST'])
@utils.validate_params('email', 'name', 'password')
def create():
    user_data = request.get_json()
    try:
        user = User(**user_data)
        g.session.add(user)
        g.session.flush()
    except IntegrityError:
        g.session.rollback()
        abort(400, "There's a user with that email registered")

    return make_response(utils.to_json(user), 201)


@user_bp.route('/', methods=['GET'])
def read():
    users = g.session.execute(select(User)).fetchall()
    return make_response(jsonify(utils.to_json(utils.flatten(users))), 200)


@user_bp.route('/<user_id>', methods=['DELETE'])
def delete(user_id: int):
    user = g.session.get(User, user_id)
    if not user:
        return make_response("User Not Found", 404)
    g.session.delete(user)
    return make_response("OK", 202)


@user_bp.route('/password/<user_id>', methods=['PATCH'])
@utils.validate_params('password')
def update_password(user_id: int):
    user_data = request.get_json()

    user = g.session.get(User, user_id)
    if not user:
        return make_response("User Not Found", 404)
    user.password = user_data['password']

    return make_response(utils.to_json(user), 202)

