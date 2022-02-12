from models import User
from json import loads
from src.config import (
    API_VERSION,
    API_ROOT
)


class TestGetUserEndpoints:

    def test_if_returns_the_user_when_id_exists_in_database(self, test_client):
        new_user = User().create(
            test_client.db.session,
            name='Test User',
            email='testuser@email.com',
            integration_id='1234'
        )
        test_client.db.session.commit()
        response = test_client.get(
            f'/{API_ROOT}/v{API_VERSION}/settings/{new_user.id}'
        )
        assert loads(response.get_data()) == dict(
            id=new_user.id,
            email='testuser@email.com',
            integration_id='1234',
            name='Test User',
        )

    def test_if_returns_404_when_id_does_not_exist_in_database(self, test_client):
        response = test_client.get(
            f'/{API_ROOT}/v{API_VERSION}/settings/999999'
        )
        assert response.status_code == 404

    def test_if_returns_user_not_found_when_id_does_not_exist_in_database(self, test_client):
        response = test_client.get(
            f'/{API_ROOT}/v{API_VERSION}/settings/999999'
        )
        assert 'Not found user' in str(response.get_data())
