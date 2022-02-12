from models import User
from mocklib import update_user
from loguru import logger


class ExternalSystemException(Exception):

    def __init__(self, message):
        super().__init__(message)
        logger.error(message)


def call_external_system(user: User):
    result = update_user(dict(
        id=user.integration_id,
        email=user.email,
        name=user.name
    ))
    if result == 'success':
        return True
    raise ExternalSystemException('Error received from external system')
