import pytest

@pytest.fixture
def new_post():
    return {
        "title": "Test titel",
        "body": "Test indhold",
        "userId": 1
    }