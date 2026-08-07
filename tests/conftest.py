import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Base
from models.user import User




TEST_DATABASE_URL = "sqlite:///test_todo.db"

test_engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(bind=test_engine)


@pytest.fixture
def db():
    Base.metadata.create_all(bind=test_engine)

    db = TestingSessionLocal()

    yield db

    db.close()
    Base.metadata.drop_all(bind=test_engine)
@pytest.fixture
def user(db):
    user = User(
        username="testuser",
        hashed_password="testpassword"
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user
