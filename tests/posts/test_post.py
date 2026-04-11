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

def test_opret_post_uden_body(new_post):
    payload = {"title": new_post["title"], "userId": new_post["userId"]}
    response = post("/posts", payload)
    assert response.status_code == 201
    assert "body" not in response.json() or response.json().get("body") == ""

def test_opret_tomt_post():
    response = post("/posts", {})
    assert response.status_code == 201

def test_valider_felter_i_response(new_post):
    response = post("/posts", new_post)
    body = response.json()
    assert response.status_code == 201
    assert all(felt in body for felt in ["id", "title", "body", "userId"])

def test_opret_post_med_lang_titel():
    payload = {"title": "a" * 500, "body": "Test indhold", "userId": 1}
    response = post("/posts", payload)
    assert response.status_code == 201
    assert len(response.json()["title"]) == 500
