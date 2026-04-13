import pytest
import allure
import requests
from tests.todo_api.conftest import BASE_URL


@pytest.mark.smoke
@pytest.mark.regression
@allure.feature("Todo API")
@allure.story("PUT")
@allure.title("Opdater todo titel")
@allure.description("Testdesign: Ækvivalenspartitionering\nBeskrivelse: Opdaterer titlen på en eksisterende todo\nForventet: HTTP 200 og titel matcher den sendte værdi")
def test_opdater_todo_titel(created_todo):
    """
    Testdesign: Ækvivalenspartitionering
    Beskrivelse: Opdaterer titlen på en eksisterende todo
    Forudsætning: Todo eksisterer i API'et
    Forventet resultat: HTTP 200 og titel matcher den sendte værdi
    """
    todo_id = created_todo["id"]
    response = requests.put(f"{BASE_URL}/todos/{todo_id}", json={"title": "Opdateret titel"})
    print(f"\nResponse: {response.json()}")
    assert response.status_code == 200
    assert response.json()["title"] == "Opdateret titel"


@pytest.mark.regression
@allure.feature("Todo API")
@allure.story("PUT")
@allure.title("Opdater todo completed status")
@allure.description("Testdesign: Ækvivalenspartitionering\nBeskrivelse: Opdaterer completed-feltet på en eksisterende todo\nForventet: HTTP 200 og completed = true")
def test_opdater_todo_completed(created_todo):
    """
    Testdesign: Ækvivalenspartitionering
    Beskrivelse: Opdaterer completed-feltet på en eksisterende todo
    Forudsætning: Todo eksisterer i API'et med completed = false
    Forventet resultat: HTTP 200 og completed = true
    """
    todo_id = created_todo["id"]
    response = requests.put(f"{BASE_URL}/todos/{todo_id}", json={"completed": True})
    assert response.status_code == 200
    assert response.json()["completed"] is True


@pytest.mark.regression
@pytest.mark.negative
@allure.feature("Todo API")
@allure.story("PUT")
@allure.title("Opdater todo der ikke findes")
@allure.description("Testdesign: Negativ test\nBeskrivelse: Forsøger at opdatere en todo med et id der ikke eksisterer\nForventet: HTTP 404")
def test_opdater_todo_der_ikke_findes():
    """
    Testdesign: Negativ test
    Beskrivelse: Forsøger at opdatere en todo med et id der ikke eksisterer
    Forudsætning: Todo med id 99999 eksisterer ikke i API'et
    Forventet resultat: HTTP 404
    """
    response = requests.put(f"{BASE_URL}/todos/99999", json={"title": "Findes ikke"})
    print(f"\nResponse status: {response.status_code}")
    assert response.status_code == 404


@pytest.mark.regression
@allure.feature("Todo API")
@allure.story("PUT")
@allure.title("Opdater todo med tomt objekt")
@allure.description("Testdesign: Ækvivalenspartitionering\nBeskrivelse: Opdaterer en todo med et tomt objekt\nForventet: HTTP 200 og todo er uændret")
def test_opdater_todo_med_tomt_objekt(created_todo):
    """
    Testdesign: Ækvivalenspartitionering
    Beskrivelse: Opdaterer en todo med et tomt objekt (ingen felter ændres)
    Forudsætning: Todo eksisterer i API'et
    Forventet resultat: HTTP 200 og todo er uændret
    """
    todo_id = created_todo["id"]
    response = requests.put(f"{BASE_URL}/todos/{todo_id}", json={})
    assert response.status_code == 200
    assert response.json()["title"] == created_todo["title"]


@pytest.mark.regression
@allure.feature("Todo API")
@allure.story("PUT")
@allure.title("Valider felter i PUT response")
@allure.description("Testdesign: Ækvivalenspartitionering\nBeskrivelse: Validerer at response indeholder alle forventede felter efter opdatering\nForventet: HTTP 200 og response indeholder id, title, completed")
def test_valider_felter_i_response(created_todo):
    """
    Testdesign: Ækvivalenspartitionering
    Beskrivelse: Validerer at response indeholder alle forventede felter efter opdatering
    Forudsætning: Todo eksisterer i API'et
    Forventet resultat: HTTP 200 og response indeholder felterne id, title, completed
    """
    todo_id = created_todo["id"]
    response = requests.put(f"{BASE_URL}/todos/{todo_id}", json={"title": "Opdateret"})
    todo = response.json()
    assert response.status_code == 200
    assert all(felt in todo for felt in ["id", "title", "completed"])
