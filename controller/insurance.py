from flask import Blueprint, request, make_response, jsonify, g, abort
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from server import utils
from server.models import Insurance, User, Insurer, Category

insurance_bp = Blueprint('insurance', __name__)


@insurance_bp.route('/', methods=['POST'])
@utils.validate_params('user_id', 'insurer_id', 'insurance_amount', 'insurance_category_id', 'regularity', 'detail',
                       'coverage_end_date')
def create():
    insurance_data = request.get_json()

    insurer = g.session.get(Insurer, insurance_data['insurer_id'])
    if not insurer:
        abort(400, f'The insurer with id: "{insurance_data["insurer_id"]}" does not exist')

    category = g.session.get(Category, insurance_data['insurance_category_id'])
    if not category:
        abort(400, f'The insurance category with id: "{insurance_data["insurance_category_id"]}" '
                   f'does not exist')
    if category not in insurer.categories:
        abort(400, f'The insurer with id: "{insurance_data["insurer_id"]}" does not work with'
                   f' insurances of category: "{insurance_data["insurance_category_id"]}"')

    try:
        insurance = Insurance(**insurance_data)
        g.session.add(insurance)
        g.session.flush()
    except IntegrityError:
        g.session.rollback()
        user = g.session.get(User, insurance_data['user_id'])
        if not user:
            abort(400, f'The user with id: "{insurance_data["user_id"]}" does not exist')

    return make_response(utils.to_json(insurance), 201)


@insurance_bp.route('/', methods=['GET'])
def read():
    users = g.session.execute(select(Insurance)).fetchall()
    return make_response(jsonify(utils.to_json(utils.flatten(users))), 200)


@insurance_bp.route('/<insurance_id>', methods=['GET'])
def details(insurance_id: int):
    insurance = g.session.get(Insurance, insurance_id)
    if not insurance:
        abort(404, "Insurer Not Found")

    insurance_data = utils.to_json(insurance)
    insurance_data.update({
        'insurer_name': insurance.insurer.name,
        'insurer_telephone': insurance.insurer.telephone,
        'insurance_category': insurance.category.name
    })

    return make_response(insurance_data, 200)


@insurance_bp.route('/<insurance_id>', methods=['DELETE'])
def delete(insurance_id: int):
    insurer = g.session.get(Insurance, insurance_id)
    if not insurer:
        abort(404, "Insurer Not Found")
    g.session.delete(insurer)
    return make_response("OK", 202)
