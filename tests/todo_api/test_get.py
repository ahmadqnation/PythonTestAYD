import pytest
import allure
import requests
from tests.todo_api.conftest import BASE_URL


@pytest.mark.smoke
@pytest.mark.regression
@allure.feature("Todo API")
@allure.story("GET")
@allure.title("Hent alle todos")
@allure.description("Testdesign: Ækvivalenspartitionering\nBeskrivelse: Henter alle todos fra /todos endpointet\nForventet: HTTP 200 og en liste med mindst én todo")
def test_hent_alle_todos(created_todo):
    """
    Testdesign: Ækvivalenspartitionering
    Beskrivelse: Henter alle todos fra /todos endpointet
    Forudsætning: API'et er tilgængeligt og indeholder mindst én todo
    Forventet resultat: HTTP 200 og en liste med mindst én todo
    """
    response = requests.get(f"{BASE_URL}/todos")
    print(f"\nResponse: {response.json()[:2]}")
    assert response.status_code == 200
    assert len(response.json()) > 0


@pytest.mark.regression
@allure.feature("Todo API")
@allure.story("GET")
@allure.title("Hent enkelt todo med gyldigt id")
@allure.description("Testdesign: Ækvivalenspartitionering\nBeskrivelse: Henter en enkelt todo med gyldigt id\nForventet: HTTP 200 og todo med korrekt id")
def test_hent_enkelt_todo(created_todo):
    """
    Testdesign: Ækvivalenspartitionering
    Beskrivelse: Henter en enkelt todo med gyldigt id
    Forudsætning: Todo eksisterer i API'et
    Forventet resultat: HTTP 200 og todo med korrekt id
    """
    todo_id = created_todo["id"]
    response = requests.get(f"{BASE_URL}/todos/{todo_id}")
    print(f"\nResponse: {response.json()}")
    assert response.status_code == 200
    assert response.json()["id"] == todo_id


@pytest.mark.regression
@pytest.mark.negative
@allure.feature("Todo API")
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
    response = requests.get(f"{BASE_URL}/todos/99999")
    print(f"\nResponse: {response.status_code}")
    assert response.status_code == 404


@pytest.mark.regression
@allure.feature("Todo API")
@allure.story("GET")
@allure.title("Valider felter i todo response")
@allure.description("Testdesign: Ækvivalenspartitionering\nBeskrivelse: Validerer at en todo indeholder alle forventede felter\nForventet: HTTP 200 og response indeholder id, title, completed")
def test_valider_felter_i_todo(created_todo):
    """
    Testdesign: Ækvivalenspartitionering
    Beskrivelse: Validerer at en todo indeholder alle forventede felter
    Forudsætning: Todo eksisterer i API'et
    Forventet resultat: HTTP 200 og response indeholder felterne id, title, completed
    """
    todo_id = created_todo["id"]
    response = requests.get(f"{BASE_URL}/todos/{todo_id}")
    todo = response.json()
    assert response.status_code == 200
    assert all(felt in todo for felt in ["id", "title", "completed"])


@pytest.mark.regression
@pytest.mark.negative
@allure.feature("Todo API")
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
    response = requests.get(f"{BASE_URL}/todos/-1")
    assert response.status_code == 404


@pytest.mark.regression
@pytest.mark.negative
@allure.feature("Todo API")
@allure.story("GET")
@allure.title("Hent todo med ugyldigt id (tekst)")
@allure.description("Testdesign: Ækvivalenspartitionering\nBeskrivelse: Forsøger at hente en todo med tekst som id (ugyldig partition)\nForventet: HTTP 422")
def test_hent_todo_med_ugyldigt_id():
    """
    Testdesign: Ækvivalenspartitionering
    Beskrivelse: Forsøger at hente en todo med tekst som id (ugyldig partition)
    Forudsætning: API'et forventer numeriske id-værdier
    Forventet resultat: HTTP 422 (FastAPI validering)
    """
    response = requests.get(f"{BASE_URL}/todos/abc")
    assert response.status_code == 422
