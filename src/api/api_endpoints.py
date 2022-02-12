from app import db
from flask_restplus import Api
from flask_restplus import Namespace, Resource, fields, abort
from werkzeug.exceptions import HTTPException
from werkzeug.exceptions import NotFound
from werkzeug.exceptions import InternalServerError
from models import User


namespace = Namespace('settings', description='Settings')


get_user_response = namespace.model('Get User Response', {
    'id': fields.Integer(required=True, description='user identifier'),
    'name': fields.String(required=True, description='user name'),
    'email': fields.String(required=True, description='user email'),
    'integration_id': fields.String(required=True, description='user exterenal integration id')
})


headers = namespace.parser()


@namespace.route('/<int:id>', doc={"description": 'Get User'})
@namespace.param('id', 'User identifier')
@namespace.expect(headers)
class GetUser(Resource):
    @namespace.response(200, 'Success')
    @namespace.response(404, 'Not Found user')
    @namespace.marshal_with(get_user_response)
    def get(self, id):
        """Get User"""
        session = db.session
        try:
            user = User().fetch(session, id)
            if not user:
                raise NotFound('Not found user')
            return user
        finally:
            session.close()


def register_endpoints(api: Api):
    """
    Make the endpoint's namespace registration into the API
    :param api: Flask Restplus API
    :return: Void
    """
    api.add_namespace(namespace)
    return None