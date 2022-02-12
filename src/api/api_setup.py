from flask import Flask, Blueprint
from flask_restplus import Api as ApiRestPlus
# from api.endpoints import _


api = ApiRestPlus(
    Blueprint('API - Skill Suite', __name__),
    title='API to manage Skill Suite system',
    version='1.0'
)

#_.bind_with_api(api)


def api_loader(app: Flask) -> None:
    """
    This method should be used to load the the blueprint API into Flask App
    :param app: Flask App
    :return: Void
    """
    app.register_blueprint(api.blueprint, url_prefix='/skillsuite/v1.0')
    return None