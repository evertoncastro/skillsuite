from app import db
from models import User
from util import is_valid_email
from flask_restplus import Api
from flask_restplus import Namespace, Resource, fields, abort
from werkzeug.exceptions import HTTPException
from werkzeug.exceptions import BadRequest
from werkzeug.exceptions import NotFound
from werkzeug.exceptions import InternalServerError
from services.external_system import (
    call_external_system,
    ExternalSystemException
)


namespace = Namespace('settings', description='Settings')


user_response = namespace.model('Get User Response', {
    'id': fields.Integer(required=True, description='user identifier'),
    'name': fields.String(required=True, description='user name'),
    'email': fields.String(required=True, description='user email'),
    'integration_id': fields.String(required=True, description='user exterenal integration id')
})


update_user_request = namespace.model('Update user request', {
    'name': fields.String(required=False, description='user name'),
    'email': fields.String(required=False, description='user email')
})



headers = namespace.parser()


@namespace.route('/<int:id>', doc={"description": 'Settings'})
@namespace.param('id', 'user identifier')
@namespace.expect(headers)
class UserSettings(Resource):
    @namespace.response(200, 'Success')
    @namespace.response(404, 'Not Found user')
    @namespace.marshal_with(user_response)
    def get(self, id):
        """Get user"""
        session = db.session
        try:
            user = User().fetch(session, id)
            if not user:
                raise NotFound('Not found user')
            return user
        finally:
            session.close()

    @namespace.response(200, 'Success')
    @namespace.response(404, 'Not Found user')
    @namespace.expect(update_user_request, validate=True)
    @namespace.marshal_with(user_response)
    def put(self, id):
        """Update user"""
        session = db.session
        try:
            # IDEA: The validation could be attatched to the fields
            data = namespace.payload
            if data.get('email') and not is_valid_email(data.get('email')):
                raise BadRequest(f'Invalid email')
            user = User().update(session, id, **data)
            if not user:
                raise NotFound('Not found user')
            call_external_system(user)
            # session.commit()
            return user
        except ExternalSystemException as e:
            session.rollback()
            raise InternalServerError(e.args[0])
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