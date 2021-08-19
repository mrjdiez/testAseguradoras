from flask import Blueprint, request, make_response, jsonify, g, abort
from sqlalchemy import select

from server import utils
from server.models import Insurer

insurer_bp = Blueprint('insurer', __name__)


@insurer_bp.route('/', methods=['POST'])
@utils.validate_params('name', 'telephone')
def create():
    insurer_data = request.get_json()
    insurer = Insurer(**insurer_data)
    g.session.add(insurer)
    g.session.flush()
    return make_response(utils.to_json(insurer), 201)


@insurer_bp.route('/', methods=['GET'])
def read():
    users = g.session.execute(select(Insurer)).fetchall()
    return make_response(jsonify(utils.to_json(utils.flatten(users))), 200)


@insurer_bp.route('/<insurer_id>', methods=['GET'])
def details(insurer_id: int):
    insurer = g.session.get(Insurer, insurer_id)
    if not insurer:
        abort(404, "Insurer Not Found")
    return make_response(utils.to_json(insurer), 200)


@insurer_bp.route('/<insurer_id>', methods=['DELETE'])
def delete(insurer_id: int):
    insurer = g.session.get(Insurer, insurer_id)
    if not insurer:
        abort(404, "Insurer Not Found")
    g.session.delete(insurer)
    return make_response("OK", 202)
