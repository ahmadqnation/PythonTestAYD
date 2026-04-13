import pytest
import requests

BASE_URL = "https://pythonayd-todo-api.onrender.com"


@pytest.fixture
def new_todo():
    return {"title": "Test todo", "completed": False}


@pytest.fixture
def created_todo(new_todo):
    response = requests.post(f"{BASE_URL}/todos", json=new_todo)
    todo = response.json()
    yield todo
    requests.delete(f"{BASE_URL}/todos/{todo['id']}")
