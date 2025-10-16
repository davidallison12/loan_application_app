import pytest
from app import create_app, db


@pytest.fixture
def client():
    app = create_app({
        "TESTING":True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"
        })
    
    with app.app_context():
        db.create_all()

        yield app.test_client()

        with app.app_context():
            db.drop_all()
