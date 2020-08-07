import pytest

from project import create_app, db

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

