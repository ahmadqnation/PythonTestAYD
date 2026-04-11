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
