from helpers.api_client import get, post

def test_hent_alle_posts():
    response = get("/posts")
    print(f"\nResponse: {response.json()[:2]}")  # Viser de første 2 posts
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_hent_enkelt_post():
    response = get("/posts/1")
    print(f"\nResponse: {response.json()}")
    assert response.status_code == 200
    assert response.json()["id"] == 1

def test_opret_post(new_post):
    response = post("/posts", new_post)
    print(f"\nResponse: {response.json()}")
    assert response.status_code == 201
    assert response.json()["title"] == "Test titel"

def test_hent_post_der_ikke_findes():
    response = get("/posts/99999")
    print(f"\nResponse: {response.status_code}")
    assert response.status_code == 404

def test_opret_post_uden_titel(new_post):
    incomplete_post = {"body": "Test indhold", "userId": 1}
    response = post("/posts", incomplete_post)
    print(f"\nResponse: {response.json()}")
    assert response.status_code == 201
    assert "title" not in response.json() or response.json().get("title") == ""

def test_hent_comments_til_post():
    response = get("/posts/1/comments")
    print(f"\nResponse: {response.json()[:2]}")
    assert response.status_code == 200
    assert len(response.json()) > 0
    assert "email" in response.json()[0]