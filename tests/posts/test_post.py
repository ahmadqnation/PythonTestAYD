from helpers.api_client import post

def test_opret_post(new_post):
    response = post("/posts", new_post)
    print(f"\nResponse: {response.json()}")
    assert response.status_code == 201
    assert response.json()["title"] == "Test titel"

def test_opret_post_uden_titel():
    incomplete_post = {"body": "Test indhold", "userId": 1}
    response = post("/posts", incomplete_post)
    print(f"\nResponse: {response.json()}")
    assert response.status_code == 201
    assert "title" not in response.json() or response.json().get("title") == ""
