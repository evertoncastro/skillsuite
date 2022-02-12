import os
import pytest
import tempfile
import contextlib
from src.main import app as test_app
from app import setup_app, db as test_db
from base64 import b64encode
from sqlalchemy import MetaData

meta = MetaData()

os.environ["ENV"] = "testing"
os.environ["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"

if os.path.exists("src/test.db"):
    os.remove("src/test.db")


@pytest.fixture(scope="session")
def app():
    """Instance of Flask App for tests"""
    return setup_app()


@pytest.fixture(scope="session")
def test_client():
    """Instance of test client for tests"""
    # Yeld test client with request context
    test_app.testing = True
    app_context = test_app.test_request_context()
    app_context.push()
    with test_app.test_client() as client:
        # Setup database
        test_db.create_all()
    client.db = test_db
    yield client
    # Clear database
    test_db.reflect()
    for table in reversed(test_db.metadata.sorted_tables):
        test_db.session.execute(table.delete())
        test_db.session.commit()
    test_db.session.close()

