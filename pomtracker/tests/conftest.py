import pytest
from pomtracker import create_app, db
from pomtracker.tests.factory import Factory


@pytest.fixture(scope="module")
def test_app():
    app = create_app()
    app.config['TESTING'] = True
    with app.app_context():
        yield app


@pytest.fixture(scope="module")
def test_db():
    db.create_all()
    yield db
    db.session.remove()
    db.drop_all()


@pytest.fixture(scope="module")
def factory():
    return Factory
