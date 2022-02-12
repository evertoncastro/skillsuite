from pytest import raises
from src.models import User
from services.external_system import (
    call_external_system,
    ExternalSystemException
)


class TestCallExternalService:

    def test_if_returns_true_after_receiving_success(self, test_client, mocker):
        user = User().create(
            test_client.db.session,
            name='Test Update Name',
            email='test150@email.com',
            integration_id='150'
        )
        mocker.patch('services.external_system.update_user', return_value='success')
        success = call_external_system(user)
        assert success

    def test_if_raises_exception_after_receiving_fail(self, test_client, mocker):
        user = User().create(
            test_client.db.session,
            name='Test Update Name',
            email='test160@email.com',
            integration_id='160'
        )
        mocker.patch('services.external_system.update_user', return_value='fail')
        with raises(ExternalSystemException) as error:
            call_external_system(user)
        assert error.value.args[0] == 'Error received from external system'
