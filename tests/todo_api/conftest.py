import pytest
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

BASE_URL = "https://pythonayd-todo-api.onrender.com"


@pytest.fixture(scope="function")
def db_session():
    database_url = os.getenv("DATABASE_URL")
    engine = create_engine(database_url)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
    engine.dispose()


@pytest.fixture
def new_todo():
    return {"title": "Test todo", "completed": False}


@pytest.fixture
def created_todo(new_todo):
    response = requests.post(f"{BASE_URL}/todos", json=new_todo)
    todo = response.json()
    yield todo
    requests.delete(f"{BASE_URL}/todos/{todo['id']}")
