import pytest
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
from api.models_db_auth import UserDB

load_dotenv()

BASE_URL = "https://pythonayd-todo-api.onrender.com"

TEST_EMAIL = "testuser@test.dk"
TEST_PASSWORD = "Test1234!"
TEST_CVR = "12345678"


@pytest.fixture(scope="function")
def db_session():
    database_url = os.getenv("DATABASE_URL")
    engine = create_engine(database_url)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
    engine.dispose()


@pytest.fixture(scope="session")
def auth_token():
    # Forsøg registrering — ignorer fejl hvis brugeren allerede findes
    requests.post(f"{BASE_URL}/auth/register", json={
        "email": TEST_EMAIL,
        "password": TEST_PASSWORD,
        "cvr": TEST_CVR,
    })
    # Login og returner access token
    response = requests.post(f"{BASE_URL}/auth/login", json={
        "email": TEST_EMAIL,
        "password": TEST_PASSWORD,
    })
    assert response.status_code == 200, f"Login fejlede: {response.text}"
    return response.json()["access_token"]


@pytest.fixture(scope="session")
def auth_headers(auth_token):
    return {"Authorization": f"Bearer {auth_token}"}


@pytest.fixture(scope="session")
def test_user_id():
    database_url = os.getenv("DATABASE_URL")
    engine = create_engine(database_url)
    Session = sessionmaker(bind=engine)
    session = Session()
    user = session.query(UserDB).filter_by(email=TEST_EMAIL).first()
    user_id = user.id
    session.close()
    engine.dispose()
    return user_id


@pytest.fixture
def new_todo():
    return {"title": "Test todo", "completed": False}


@pytest.fixture
def created_todo(new_todo, auth_headers):
    response = requests.post(f"{BASE_URL}/todos", json=new_todo, headers=auth_headers)
    todo = response.json()
    yield todo
    requests.delete(f"{BASE_URL}/todos/{todo['id']}", headers=auth_headers)
