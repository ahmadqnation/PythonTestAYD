from helpers.api_client import put

def test_opdater_post(new_post):
    """
    Testdesign: Ækvivalenspartitionering
    Beskrivelse: Opdaterer et eksisterende post med alle gyldige felter
    Forudsætning: Post med id 1 eksisterer i API'et
    Forventet resultat: HTTP 200, titel og id matcher de sendte værdier
    """
    opdateret = {**new_post, "title": "Opdateret titel", "id": 1}
    response = put("/posts/1", opdateret)
    print(f"\nResponse: {response.json()}")
    assert response.status_code == 200
    assert response.json()["title"] == "Opdateret titel"
    assert response.json()["id"] == 1

def test_opdater_post_kun_titel():
    """
    Testdesign: Ækvivalenspartitionering
    Beskrivelse: Opdaterer et post med kun titel specificeret
    Forudsætning: Post med id 1 eksisterer i API'et
    Forventet resultat: HTTP 200 og titel matcher den sendte værdi
    """
    payload = {"title": "Ny titel", "body": "Eksisterende indhold", "userId": 1, "id": 1}
    response = put("/posts/1", payload)
    print(f"\nResponse: {response.json()}")
    assert response.status_code == 200
    assert response.json()["title"] == "Ny titel"

def test_opdater_post_der_ikke_findes(new_post):
    """
    Testdesign: Negativ test
    Beskrivelse: Forsøger at opdatere et post med et id der ikke eksisterer
    Forudsætning: Post med id 99999 eksisterer ikke i API'et
    Forventet resultat: HTTP 404 eller 500
    """
    response = put("/posts/99999", {**new_post, "id": 99999})
    print(f"\nResponse status: {response.status_code}")
    # JSONPlaceholder returnerer 500 for ikke-eksisterende ressourcer ved PUT
    assert response.status_code in [404, 500]

def test_opdater_post_uden_body(new_post):
    """
    Testdesign: Ækvivalenspartitionering
    Beskrivelse: Opdaterer et post uden body-feltet (ugyldig partition)
    Forudsætning: Post med id 1 eksisterer i API'et
    Forventet resultat: HTTP 200 og body er fraværende eller tom i response
    """
    payload = {"title": new_post["title"], "userId": new_post["userId"], "id": 1}
    response = put("/posts/1", payload)
    assert response.status_code == 200
    assert "body" not in response.json() or response.json().get("body") == ""

def test_opdater_tomt_post():
    """
    Testdesign: Ækvivalenspartitionering
    Beskrivelse: Opdaterer et post med et tomt objekt (ugyldig partition)
    Forudsætning: Post med id 1 eksisterer i API'et
    Forventet resultat: HTTP 200 — JSONPlaceholder validerer ikke felter
    """
    response = put("/posts/1", {})
    assert response.status_code == 200

def test_opdater_sidste_gyldige_post(new_post):
    """
    Testdesign: Grænseværdianalyse
    Beskrivelse: Opdaterer det sidste gyldige post ved øvre grænse (id = 100)
    Forudsætning: API'et indeholder præcis 100 posts
    Forventet resultat: HTTP 200 og id i response er 100
    """
    payload = {**new_post, "id": 100}
    response = put("/posts/100", payload)
    assert response.status_code == 200
    assert response.json()["id"] == 100

def test_valider_felter_i_response(new_post):
    """
    Testdesign: Ækvivalenspartitionering
    Beskrivelse: Validerer at response indeholder alle forventede felter efter opdatering
    Forudsætning: Post med id 1 eksisterer i API'et og new_post fixture er defineret
    Forventet resultat: HTTP 200 og response indeholder felterne id, title, body, userId
    """
    payload = {**new_post, "title": "Opdateret titel", "id": 1}
    response = put("/posts/1", payload)
    body = response.json()
    assert response.status_code == 200
    assert all(felt in body for felt in ["id", "title", "body", "userId"])
