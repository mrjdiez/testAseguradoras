import json
import os


from controller.user import user_bp
from controller.insurer import insurer_bp
from controller.insurance import insurance_bp
from server import models

from flask import Flask, make_response, g
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session
from sqlalchemy.engine import Engine
from werkzeug.exceptions import HTTPException


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


app = Flask(__name__)
db_file = 'database.db'
engine = create_engine(f'sqlite+pysqlite:///{db_file}')


@app.route('/health-check', methods=['GET'])
def health_check():
    return make_response("OK", 200)


app.register_blueprint(user_bp, url_prefix='/api/users')
app.register_blueprint(insurer_bp, url_prefix='/api/insurers')
app.register_blueprint(insurance_bp, url_prefix='/api/insurances')


@app.before_request
def _prepare_request():
    g.session = Session(engine, autoflush=True)


@app.after_request
def _after_request(response):
    session: Session = g.session
    session.commit()
    session.flush()
    session.close()
    return response


@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response


models.mapper_registry.metadata.create_all(engine)


@app.cli.command('reset-db')
def reset_db():
    if os.path.isfile(db_file):
        os.remove(db_file)
    models.mapper_registry.metadata.create_all(engine)
    base_insurers_path = 'aseguradoras.json'
    if not os.path.isfile(base_insurers_path):
        raise EnvironmentError("No existe el fichero de aseguradoras")

    session = Session(engine)
    car = models.Category(name='Coche')
    bike = models.Category(name='Moto')
    session.add(car)
    session.add(bike)
    categories = {'Coche': car, 'Moto': bike}

    for insurer in json.load(open(base_insurers_path, 'r')):
        session.add(models.Insurer(
            name=insurer['nombre'],
            telephone=insurer['tlf'],
            categories=[categories[cat] for cat in insurer['categorias']]
        ))

    session.commit()


if __name__ == '__main__':

    app.run()
