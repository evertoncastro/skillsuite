
from models import User
from app import db


class TestUserModel:

    def test_if_create_user_with_success(self, test_client):
        new_user = User().create(
            test_client.db.session,
            name='Test User 1',
            email='testuser1@email.com',
            integration_id='123'
        )
        test_client.db.session.commit()
        test_user = test_client.db.session.query(User).filter_by(
            id=new_user.id
        ).first()
        assert test_user

    def test_if_get_user_that_exists_in_database(self, test_client):
        new_user = User().create(
            test_client.db.session,
            name='Test User 2',
            email='testuser2@email.com',
            integration_id='1234'
        )
        test_client.db.session.commit()
        test_user = User().fetch(test_client.db.session, new_user.id)
        assert test_user.email == 'testuser2@email.com'