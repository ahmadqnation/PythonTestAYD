import pytest
import allure
from helpers.api_client import get


@pytest.mark.smoke
@pytest.mark.regression
@allure.feature("Todos API")
@allure.story("GET")
@allure.title("Hent alle todos")
@allure.description("Testdesign: Ækvivalenspartitionering\nBeskrivelse: Henter alle todos fra /todos endpointet\nForventet: HTTP 200 og en liste med mindst én todo")
def test_hent_alle_todos():
    """
    Testdesign: Ækvivalenspartitionering
    Beskrivelse: Henter alle todos fra /todos endpointet
    Forudsætning: API'et er tilgængeligt og indeholder todos
    Forventet resultat: HTTP 200 og en liste med mindst én todo
    """
    response = get("/todos")
    print(f"\nResponse: {response.json()[:2]}")
    assert response.status_code == 200
    assert len(response.json()) > 0


@pytest.mark.regression
@allure.feature("Todos API")
@allure.story("GET")
@allure.title("Hent enkelt todo med gyldigt id")
@allure.description("Testdesign: Ækvivalenspartitionering\nBeskrivelse: Henter en enkelt todo med gyldigt id\nForventet: HTTP 200 og todo med id = 1")
def test_hent_enkelt_todo():
    """
    Testdesign: Ækvivalenspartitionering
    Beskrivelse: Henter en enkelt todo med gyldigt id
    Forudsætning: Todo med id 1 eksisterer i API'et
    Forventet resultat: HTTP 200 og en todo med id = 1
    """
    response = get("/todos/1")
    print(f"\nResponse: {response.json()}")
    assert response.status_code == 200
    assert response.json()["id"] == 1


@pytest.mark.regression
@pytest.mark.negative
@allure.feature("Todos API")
@allure.story("GET")
@allure.title("Hent todo der ikke findes")
@allure.description("Testdesign: Negativ test\nBeskrivelse: Forsøger at hente en todo med et id der ikke eksisterer\nForventet: HTTP 404")
def test_hent_todo_der_ikke_findes():
    """
    Testdesign: Negativ test
    Beskrivelse: Forsøger at hente en todo med et id der ikke eksisterer
    Forudsætning: Todo med id 99999 eksisterer ikke i API'et
    Forventet resultat: HTTP 404
    """
    response = get("/todos/99999")
    print(f"\nResponse: {response.status_code}")
    assert response.status_code == 404


@pytest.mark.regression
@allure.feature("Todos API")
@allure.story("GET")
@allure.title("Hent sidste gyldige todo (id = 200)")
@allure.description("Testdesign: Grænseværdianalyse\nBeskrivelse: Henter den sidste gyldige todo ved øvre grænse (id = 200)\nForventet: HTTP 200")
def test_hent_sidste_gyldige_todo():
    """
    Testdesign: Grænseværdianalyse
    Beskrivelse: Henter den sidste gyldige todo ved øvre grænse (id = 200)
    Forudsætning: API'et indeholder præcis 200 todos
    Forventet resultat: HTTP 200
    """
    response = get("/todos/200")
    assert response.status_code == 200


@pytest.mark.regression
@pytest.mark.negative
@allure.feature("Todos API")
@allure.story("GET")
@allure.title("Hent todo med negativt id")
@allure.description("Testdesign: Grænseværdianalyse\nBeskrivelse: Forsøger at hente en todo med negativt id (under nedre grænse)\nForventet: HTTP 404")
def test_hent_todo_med_negativt_id():
    """
    Testdesign: Grænseværdianalyse
    Beskrivelse: Forsøger at hente en todo med negativt id (under nedre grænse)
    Forudsætning: API'et accepterer ikke negative id-værdier
    Forventet resultat: HTTP 404
    """
    response = get("/todos/-1")
    assert response.status_code == 404


@pytest.mark.regression
@pytest.mark.negative
@allure.feature("Todos API")
@allure.story("GET")
@allure.title("Hent todo med tekst som id")
@allure.description("Testdesign: Ækvivalenspartitionering\nBeskrivelse: Forsøger at hente en todo med tekst som id (ugyldig partition)\nForventet: HTTP 404")
def test_hent_todo_med_tekst_som_id():
    """
    Testdesign: Ækvivalenspartitionering
    Beskrivelse: Forsøger at hente en todo med tekst som id (ugyldig partition)
    Forudsætning: API'et forventer numeriske id-værdier
    Forventet resultat: HTTP 404
    """
    response = get("/todos/abc")
    assert response.status_code == 404


@pytest.mark.regression
@allure.feature("Todos API")
@allure.story("GET")
@allure.title("Valider felter i todo response")
@allure.description("Testdesign: Ækvivalenspartitionering\nBeskrivelse: Validerer at en todo indeholder alle forventede felter\nForventet: HTTP 200 og response indeholder id, userId, title, completed")
def test_valider_felter_i_todo():
    """
    Testdesign: Ækvivalenspartitionering
    Beskrivelse: Validerer at en todo indeholder alle forventede felter
    Forudsætning: Todo med id 1 eksisterer i API'et
    Forventet resultat: HTTP 200 og response indeholder felterne id, userId, title, completed
    """
    response = get("/todos/1")
    todo = response.json()
    assert response.status_code == 200
    assert all(felt in todo for felt in ["id", "userId", "title", "completed"])
