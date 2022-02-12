from models import User
from json import loads
from src.config import (
    API_VERSION,
    API_ROOT
)


class TestGetUserEndpoint:

    def test_if_returns_404_when_id_does_not_exist_in_database(self, test_client):
        response = test_client.get(
            f'/{API_ROOT}/v{API_VERSION}/settings/user/999999'
        )
        assert response.status_code == 404

    def test_if_returns_not_found_user_when_id_does_not_exist_in_database(self, test_client):
        response = test_client.get(
            f'/{API_ROOT}/v{API_VERSION}/settings/user/999999'
        )
        assert 'Not found user' in str(response.get_data())

    def test_if_returns_the_user_when_id_exists_in_database(self, test_client):
        new_user = User().create(
            test_client.db.session,
            name='Test User',
            email='testuser@email.com',
            integration_id='1234'
        )
        test_client.db.session.flush()
        response = test_client.get(
            f'/{API_ROOT}/v{API_VERSION}/settings/user/{new_user.id}'
        )
        assert loads(response.get_data()) == dict(
            id=new_user.id,
            email='testuser@email.com',
            integration_id='1234',
            name='Test User',
        )


class TestUpdateUserEndpoint:

    def test_if_returns_404_when_user_id_does_not_exist_in_database(self, test_client):
        response = test_client.put(
            f'/{API_ROOT}/v{API_VERSION}/settings/user/999999',
            json=dict(email='newemail@gmail.com')
        )
        assert response.status_code == 404

    def test_if_returns_not_found_user_when_user_id_does_not_exist_in_database(self, test_client):
        response = test_client.put(
            f'/{API_ROOT}/v{API_VERSION}/settings/user/999999',
            json=dict(email='newemail@gmail.com')
        )
        assert 'Not found user' in str(response.get_data())

    def test_if_receives_bad_request_for_invalid_email(self, test_client):
        response = test_client.put(
            f'/{API_ROOT}/v{API_VERSION}/settings/user/999',
            json=dict(email='invalid_email')
        )
        assert loads(response.get_data()) == dict(
            message='Invalid email'
        )

    def test_if_updates_user_name(self, test_client, mocker):
        user = User().create(
            test_client.db.session,
            name='Test Update Name',
            email='test_email@email.com',
            integration_id='145'
        )
        test_client.db.session.commit()
        mocker.patch('services.external_system.update_user', return_value='success')
        response = test_client.put(
            f'/{API_ROOT}/v{API_VERSION}/settings/user/{user.id}',
            json=dict(name='Test Updated to New Name')
        )
        assert loads(response.get_data())['name'] == 'Test Updated to New Name'

    def test_if_updates_user_email(self, test_client, mocker):
        user = User().create(
            test_client.db.session,
            name='Test Name',
            email='test_update@email.com',
            integration_id='145'
        )
        test_client.db.session.commit()
        mocker.patch('services.external_system.update_user', return_value='success')
        response = test_client.put(
            f'/{API_ROOT}/v{API_VERSION}/settings/user/{user.id}',
            json=dict(email='test_new@email.com')
        )
        assert loads(response.get_data())['email'] == 'test_new@email.com'


    def test_if_receives_error_after_failure_from_external_system(self, test_client, mocker):
        user = User().create(
            test_client.db.session,
            name='Test Name',
            email='test_update_fail@email.com',
            integration_id='500'
        )
        test_client.db.session.commit()
        mocker.patch('services.external_system.update_user', return_value='fail')
        response = test_client.put(
            f'/{API_ROOT}/v{API_VERSION}/settings/user/{user.id}',
            json=dict(name='Test Fail')
        )
        assert loads(response.get_data()) == dict(
            message='Error received from external system'
        )
