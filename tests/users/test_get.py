import pytest
import allure
from helpers.api_client import get


@pytest.mark.smoke
@pytest.mark.regression
@allure.feature("Users API")
@allure.story("GET")
@allure.title("Hent alle users")
@allure.description("Testdesign: Ækvivalenspartitionering\nBeskrivelse: Henter alle users fra /users endpointet\nForventet: HTTP 200 og en liste med mindst én bruger")
def test_hent_alle_users():
    """
    Testdesign: Ækvivalenspartitionering
    Beskrivelse: Henter alle users fra /users endpointet
    Forudsætning: API'et er tilgængeligt og indeholder users
    Forventet resultat: HTTP 200 og en liste med mindst én bruger
    """
    response = get("/users")
    print(f"\nResponse: {response.json()[:2]}")
    assert response.status_code == 200
    assert len(response.json()) > 0


@pytest.mark.regression
@allure.feature("Users API")
@allure.story("GET")
@allure.title("Hent enkelt user med gyldigt id")
@allure.description("Testdesign: Ækvivalenspartitionering\nBeskrivelse: Henter en enkelt user med gyldigt id\nForventet: HTTP 200 og user med id = 1")
def test_hent_enkelt_user():
    """
    Testdesign: Ækvivalenspartitionering
    Beskrivelse: Henter en enkelt user med gyldigt id
    Forudsætning: User med id 1 eksisterer i API'et
    Forventet resultat: HTTP 200 og en user med id = 1
    """
    response = get("/users/1")
    print(f"\nResponse: {response.json()}")
    assert response.status_code == 200
    assert response.json()["id"] == 1


@pytest.mark.regression
@pytest.mark.negative
@allure.feature("Users API")
@allure.story("GET")
@allure.title("Hent user der ikke findes")
@allure.description("Testdesign: Negativ test\nBeskrivelse: Forsøger at hente en user med et id der ikke eksisterer\nForventet: HTTP 404")
def test_hent_user_der_ikke_findes():
    """
    Testdesign: Negativ test
    Beskrivelse: Forsøger at hente en user med et id der ikke eksisterer
    Forudsætning: User med id 99999 eksisterer ikke i API'et
    Forventet resultat: HTTP 404
    """
    response = get("/users/99999")
    print(f"\nResponse: {response.status_code}")
    assert response.status_code == 404


@pytest.mark.regression
@allure.feature("Users API")
@allure.story("GET")
@allure.title("Hent sidste gyldige user (id = 10)")
@allure.description("Testdesign: Grænseværdianalyse\nBeskrivelse: Henter den sidste gyldige user ved øvre grænse (id = 10)\nForventet: HTTP 200")
def test_hent_sidste_gyldige_user():
    """
    Testdesign: Grænseværdianalyse
    Beskrivelse: Henter den sidste gyldige user ved øvre grænse (id = 10)
    Forudsætning: API'et indeholder præcis 10 users
    Forventet resultat: HTTP 200
    """
    response = get("/users/10")
    assert response.status_code == 200


@pytest.mark.regression
@pytest.mark.negative
@allure.feature("Users API")
@allure.story("GET")
@allure.title("Hent user med negativt id")
@allure.description("Testdesign: Grænseværdianalyse\nBeskrivelse: Forsøger at hente en user med negativt id (under nedre grænse)\nForventet: HTTP 404")
def test_hent_user_med_negativt_id():
    """
    Testdesign: Grænseværdianalyse
    Beskrivelse: Forsøger at hente en user med negativt id (under nedre grænse)
    Forudsætning: API'et accepterer ikke negative id-værdier
    Forventet resultat: HTTP 404
    """
    response = get("/users/-1")
    assert response.status_code == 404


@pytest.mark.regression
@pytest.mark.negative
@allure.feature("Users API")
@allure.story("GET")
@allure.title("Hent user med tekst som id")
@allure.description("Testdesign: Ækvivalenspartitionering\nBeskrivelse: Forsøger at hente en user med tekst som id (ugyldig partition)\nForventet: HTTP 404")
def test_hent_user_med_tekst_som_id():
    """
    Testdesign: Ækvivalenspartitionering
    Beskrivelse: Forsøger at hente en user med tekst som id (ugyldig partition)
    Forudsætning: API'et forventer numeriske id-værdier
    Forventet resultat: HTTP 404
    """
    response = get("/users/abc")
    assert response.status_code == 404


@pytest.mark.regression
@allure.feature("Users API")
@allure.story("GET")
@allure.title("Valider felter i user response")
@allure.description("Testdesign: Ækvivalenspartitionering\nBeskrivelse: Validerer at en user indeholder alle forventede felter\nForventet: HTTP 200 og response indeholder id, name, username, email")
def test_valider_felter_i_user():
    """
    Testdesign: Ækvivalenspartitionering
    Beskrivelse: Validerer at en user indeholder alle forventede felter
    Forudsætning: User med id 1 eksisterer i API'et
    Forventet resultat: HTTP 200 og response indeholder felterne id, name, username, email
    """
    response = get("/users/1")
    user = response.json()
    assert response.status_code == 200
    assert all(felt in user for felt in ["id", "name", "username", "email"])


@pytest.mark.regression
@allure.feature("Users API")
@allure.story("GET")
@allure.title("Hent posts for en user")
@allure.description("Testdesign: Ækvivalenspartitionering\nBeskrivelse: Henter posts tilknyttet en gyldig user\nForventet: HTTP 200 og mindst ét post")
def test_hent_posts_for_user():
    """
    Testdesign: Ækvivalenspartitionering
    Beskrivelse: Henter posts tilknyttet en gyldig user
    Forudsætning: User med id 1 eksisterer og har posts
    Forventet resultat: HTTP 200 og mindst ét post
    """
    response = get("/users/1/posts")
    print(f"\nResponse: {response.json()[:2]}")
    assert response.status_code == 200
    assert len(response.json()) > 0
