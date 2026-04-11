from helpers.api_client import get

def test_hent_alle_posts():
    response = get("/posts")
    print(f"\nResponse: {response.json()[:2]}")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_hent_enkelt_post():
    response = get("/posts/1")
    print(f"\nResponse: {response.json()}")
    assert response.status_code == 200
    assert response.json()["id"] == 1

def test_hent_post_der_ikke_findes():
    response = get("/posts/99999")
    print(f"\nResponse: {response.status_code}")
    assert response.status_code == 404

def test_hent_comments_til_post():
    response = get("/posts/1/comments")
    print(f"\nResponse: {response.json()[:2]}")
    assert response.status_code == 200
    assert len(response.json()) > 0
    assert "email" in response.json()[0]
