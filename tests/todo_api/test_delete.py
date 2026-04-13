import pytest
import allure
import requests
from tests.todo_api.conftest import BASE_URL


@pytest.mark.smoke
@pytest.mark.regression
@allure.feature("Todo API")
@allure.story("DELETE")
@allure.title("Slet eksisterende todo")
@allure.description("Testdesign: Ækvivalenspartitionering\nBeskrivelse: Sletter en eksisterende todo med gyldigt id\nForventet: HTTP 200")
def test_slet_todo(new_todo):
    """
    Testdesign: Ækvivalenspartitionering
    Beskrivelse: Sletter en eksisterende todo med gyldigt id
    Forudsætning: Todo eksisterer i API'et
    Forventet resultat: HTTP 200
    """
    created = requests.post(f"{BASE_URL}/todos", json=new_todo).json()
    response = requests.delete(f"{BASE_URL}/todos/{created['id']}")
    print(f"\nResponse status: {response.status_code}")
    assert response.status_code == 200


@pytest.mark.regression
@pytest.mark.negative
@allure.feature("Todo API")
@allure.story("DELETE")
@allure.title("Slet todo der ikke findes")
@allure.description("Testdesign: Negativ test\nBeskrivelse: Forsøger at slette en todo med et id der ikke eksisterer\nForventet: HTTP 404")
def test_slet_todo_der_ikke_findes():
    """
    Testdesign: Negativ test
    Beskrivelse: Forsøger at slette en todo med et id der ikke eksisterer
    Forudsætning: Todo med id 99999 eksisterer ikke i API'et
    Forventet resultat: HTTP 404
    """
    response = requests.delete(f"{BASE_URL}/todos/99999")
    print(f"\nResponse status: {response.status_code}")
    assert response.status_code == 404


@pytest.mark.regression
@allure.feature("Todo API")
@allure.story("DELETE")
@allure.title("Valider tomt response ved DELETE")
@allure.description("Testdesign: Ækvivalenspartitionering\nBeskrivelse: Validerer at response ved DELETE er et tomt objekt\nForventet: HTTP 200 og response body er {}")
def test_valider_tomt_response(new_todo):
    """
    Testdesign: Ækvivalenspartitionering
    Beskrivelse: Validerer at response ved DELETE er et tomt objekt
    Forudsætning: Todo eksisterer i API'et
    Forventet resultat: HTTP 200 og response body er {}
    """
    created = requests.post(f"{BASE_URL}/todos", json=new_todo).json()
    response = requests.delete(f"{BASE_URL}/todos/{created['id']}")
    assert response.status_code == 200
    assert response.json() == {}
