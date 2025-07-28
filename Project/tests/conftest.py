import pytest
from app import app as flask_app

@pytest.fixture(scope="session")
def app():
    flask_app.config.update({
        "TESTING": True
    })
    yield flask_app

@pytest.fixture(scope="function")
def client(app):
    return app.test_client()
