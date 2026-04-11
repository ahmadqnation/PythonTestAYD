from helpers.api_client import put

def test_opdater_post(new_post):
    opdateret = {**new_post, "title": "Opdateret titel", "id": 1}
    response = put("/posts/1", opdateret)
    print(f"\nResponse: {response.json()}")
    assert response.status_code == 200
    assert response.json()["title"] == "Opdateret titel"
    assert response.json()["id"] == 1

def test_opdater_post_kun_titel():
    payload = {"title": "Ny titel", "body": "Eksisterende indhold", "userId": 1, "id": 1}
    response = put("/posts/1", payload)
    print(f"\nResponse: {response.json()}")
    assert response.status_code == 200
    assert response.json()["title"] == "Ny titel"

def test_opdater_post_der_ikke_findes(new_post):
    response = put("/posts/99999", {**new_post, "id": 99999})
    print(f"\nResponse status: {response.status_code}")
    # JSONPlaceholder returnerer 500 for ikke-eksisterende ressourcer ved PUT
    assert response.status_code in [404, 500]

def test_opdater_post_uden_body(new_post):
    payload = {"title": new_post["title"], "userId": new_post["userId"], "id": 1}
    response = put("/posts/1", payload)
    assert response.status_code == 200
    assert "body" not in response.json() or response.json().get("body") == ""

def test_opdater_tomt_post():
    response = put("/posts/1", {})
    assert response.status_code == 200

def test_opdater_sidste_gyldige_post(new_post):
    payload = {**new_post, "id": 100}
    response = put("/posts/100", payload)
    assert response.status_code == 200
    assert response.json()["id"] == 100

def test_valider_felter_i_response(new_post):
    payload = {**new_post, "title": "Opdateret titel", "id": 1}
    response = put("/posts/1", payload)
    body = response.json()
    assert response.status_code == 200
    assert all(felt in body for felt in ["id", "title", "body", "userId"])
