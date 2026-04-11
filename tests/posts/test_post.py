from helpers.api_client import post

def test_opret_post(new_post):
    """
    Testdesign: Ækvivalenspartitionering
    Beskrivelse: Opretter et post med alle gyldige felter
    Forudsætning: API'et er tilgængeligt og accepterer POST requests
    Forventet resultat: HTTP 201 og response indeholder den sendte titel
    """
    response = post("/posts", new_post)
    print(f"\nResponse: {response.json()}")
    assert response.status_code == 201
    assert response.json()["title"] == "Test titel"

def test_opret_post_uden_titel():
    """
    Testdesign: Ækvivalenspartitionering
    Beskrivelse: Opretter et post uden titel-feltet (ugyldig partition)
    Forudsætning: API'et er tilgængeligt
    Forventet resultat: HTTP 201 og title er fraværende eller tom i response
    """
    incomplete_post = {"body": "Test indhold", "userId": 1}
    response = post("/posts", incomplete_post)
    print(f"\nResponse: {response.json()}")
    assert response.status_code == 201
    assert "title" not in response.json() or response.json().get("title") == ""

def test_opret_post_uden_body(new_post):
    """
    Testdesign: Ækvivalenspartitionering
    Beskrivelse: Opretter et post uden body-feltet (ugyldig partition)
    Forudsætning: API'et er tilgængeligt
    Forventet resultat: HTTP 201 og body er fraværende eller tom i response
    """
    payload = {"title": new_post["title"], "userId": new_post["userId"]}
    response = post("/posts", payload)
    assert response.status_code == 201
    assert "body" not in response.json() or response.json().get("body") == ""

def test_opret_tomt_post():
    """
    Testdesign: Ækvivalenspartitionering
    Beskrivelse: Opretter et post med et tomt objekt (ugyldig partition)
    Forudsætning: API'et er tilgængeligt
    Forventet resultat: HTTP 201 — JSONPlaceholder validerer ikke felter
    """
    response = post("/posts", {})
    assert response.status_code == 201

def test_valider_felter_i_response(new_post):
    """
    Testdesign: Ækvivalenspartitionering
    Beskrivelse: Validerer at response indeholder alle forventede felter efter oprettelse
    Forudsætning: API'et er tilgængeligt og new_post fixture er defineret
    Forventet resultat: HTTP 201 og response indeholder felterne id, title, body, userId
    """
    response = post("/posts", new_post)
    body = response.json()
    assert response.status_code == 201
    assert all(felt in body for felt in ["id", "title", "body", "userId"])

def test_opret_post_med_lang_titel():
    """
    Testdesign: Grænseværdianalyse
    Beskrivelse: Opretter et post med en titel på 500 tegn (øvre grænse)
    Forudsætning: API'et er tilgængeligt
    Forventet resultat: HTTP 201 og titel i response er 500 tegn lang
    """
    payload = {"title": "a" * 500, "body": "Test indhold", "userId": 1}
    response = post("/posts", payload)
    assert response.status_code == 201
    assert len(response.json()["title"]) == 500
