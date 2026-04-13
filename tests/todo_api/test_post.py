import pytest
import allure
import requests
from tests.todo_api.conftest import BASE_URL


@pytest.mark.smoke
@pytest.mark.regression
@allure.feature("Todo API")
@allure.story("POST")
@allure.title("Opret todo med alle gyldige felter")
@allure.description("Testdesign: Ækvivalenspartitionering\nBeskrivelse: Opretter en todo med alle gyldige felter\nForventet: HTTP 201 og response indeholder den sendte titel")
def test_opret_todo(new_todo):
    """
    Testdesign: Ækvivalenspartitionering
    Beskrivelse: Opretter en todo med alle gyldige felter
    Forudsætning: API'et er tilgængeligt og accepterer POST requests
    Forventet resultat: HTTP 201 og response indeholder den sendte titel
    """
    response = requests.post(f"{BASE_URL}/todos", json=new_todo)
    todo = response.json()
    print(f"\nResponse: {todo}")
    assert response.status_code == 201
    assert todo["title"] == new_todo["title"]
    requests.delete(f"{BASE_URL}/todos/{todo['id']}")


@pytest.mark.regression
@pytest.mark.negative
@allure.feature("Todo API")
@allure.story("POST")
@allure.title("Opret todo uden titel")
@allure.description("Testdesign: Negativ test\nBeskrivelse: Forsøger at oprette en todo uden det påkrævede titel-felt\nForventet: HTTP 422")
def test_opret_todo_uden_titel():
    """
    Testdesign: Negativ test
    Beskrivelse: Forsøger at oprette en todo uden det påkrævede titel-felt
    Forudsætning: API'et kræver title-feltet
    Forventet resultat: HTTP 422 (FastAPI validering)
    """
    response = requests.post(f"{BASE_URL}/todos", json={"completed": False})
    print(f"\nResponse: {response.status_code}")
    assert response.status_code == 422


@pytest.mark.regression
@allure.feature("Todo API")
@allure.story("POST")
@allure.title("Opret todo med completed false som default")
@allure.description("Testdesign: Ækvivalenspartitionering\nBeskrivelse: Opretter en todo uden completed-feltet og verificerer default-værdien\nForventet: HTTP 201 og completed = false")
def test_opret_todo_completed_false_som_default():
    """
    Testdesign: Ækvivalenspartitionering
    Beskrivelse: Opretter en todo uden completed-feltet og verificerer default-værdien
    Forudsætning: API'et sætter completed til false som standard
    Forventet resultat: HTTP 201 og completed = false
    """
    response = requests.post(f"{BASE_URL}/todos", json={"title": "Default completed test"})
    todo = response.json()
    assert response.status_code == 201
    assert todo["completed"] is False
    requests.delete(f"{BASE_URL}/todos/{todo['id']}")


@pytest.mark.regression
@allure.feature("Todo API")
@allure.story("POST")
@allure.title("Opret todo med completed true")
@allure.description("Testdesign: Ækvivalenspartitionering\nBeskrivelse: Opretter en todo med completed sat til true\nForventet: HTTP 201 og completed = true")
def test_opret_todo_med_completed_true():
    """
    Testdesign: Ækvivalenspartitionering
    Beskrivelse: Opretter en todo med completed sat til true
    Forudsætning: API'et accepterer completed = true
    Forventet resultat: HTTP 201 og completed = true
    """
    response = requests.post(f"{BASE_URL}/todos", json={"title": "Færdig todo", "completed": True})
    todo = response.json()
    assert response.status_code == 201
    assert todo["completed"] is True
    requests.delete(f"{BASE_URL}/todos/{todo['id']}")


@pytest.mark.regression
@allure.feature("Todo API")
@allure.story("POST")
@allure.title("Valider felter i POST response")
@allure.description("Testdesign: Ækvivalenspartitionering\nBeskrivelse: Validerer at response indeholder alle forventede felter efter oprettelse\nForventet: HTTP 201 og response indeholder id, title, completed")
def test_valider_felter_i_response(new_todo):
    """
    Testdesign: Ækvivalenspartitionering
    Beskrivelse: Validerer at response indeholder alle forventede felter efter oprettelse
    Forudsætning: API'et er tilgængeligt
    Forventet resultat: HTTP 201 og response indeholder felterne id, title, completed
    """
    response = requests.post(f"{BASE_URL}/todos", json=new_todo)
    todo = response.json()
    assert response.status_code == 201
    assert all(felt in todo for felt in ["id", "title", "completed"])
    requests.delete(f"{BASE_URL}/todos/{todo['id']}")


@pytest.mark.regression
@allure.feature("Todo API")
@allure.story("POST")
@allure.title("Opret todo med lang titel (500 tegn)")
@allure.description("Testdesign: Grænseværdianalyse\nBeskrivelse: Opretter en todo med en titel på 500 tegn (øvre grænse)\nForventet: HTTP 201 og titel i response er 500 tegn lang")
def test_opret_todo_med_lang_titel():
    """
    Testdesign: Grænseværdianalyse
    Beskrivelse: Opretter en todo med en titel på 500 tegn (øvre grænse)
    Forudsætning: API'et accepterer lange titler
    Forventet resultat: HTTP 201 og titel i response er 500 tegn lang
    """
    lang_titel = "a" * 500
    response = requests.post(f"{BASE_URL}/todos", json={"title": lang_titel})
    todo = response.json()
    assert response.status_code == 201
    assert len(todo["title"]) == 500
    requests.delete(f"{BASE_URL}/todos/{todo['id']}")
