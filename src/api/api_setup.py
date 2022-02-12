from config import (
    API_VERSION,
    API_ROOT
)
from flask import Flask, Blueprint
from flask_restplus import Api as ApiRestPlus
from api.api_endpoints import register_endpoints


api = ApiRestPlus(
    Blueprint('API - Skill Suite', __name__),
    title='API to manage Skill Suite application',
    version=API_VERSION
)

register_endpoints(api)


def api_loader(app: Flask) -> None:
    """
    This method should be used to load the the blueprint API into Flask App
    :param app: Flask App
    :return: Void
    """
    app.register_blueprint(api.blueprint, url_prefix=f'/{API_ROOT}/v{API_VERSION}')
    return None