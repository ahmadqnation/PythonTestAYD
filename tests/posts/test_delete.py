import pytest
import allure
from helpers.api_client import delete


@pytest.mark.smoke
@pytest.mark.regression
@allure.feature("Posts API")
@allure.story("DELETE")
@allure.title("Slet eksisterende post")
@allure.description("Testdesign: Ækvivalenspartitionering\nBeskrivelse: Sletter et eksisterende post med gyldigt id\nForventet: HTTP 200")
def test_slet_post():
    """
    Testdesign: Ækvivalenspartitionering
    Beskrivelse: Sletter et eksisterende post med gyldigt id
    Forudsætning: Post med id 1 eksisterer i API'et
    Forventet resultat: HTTP 200
    """
    response = delete("/posts/1")
    print(f"\nResponse status: {response.status_code}")
    assert response.status_code == 200


@pytest.mark.regression
@pytest.mark.negative
@allure.feature("Posts API")
@allure.story("DELETE")
@allure.title("Slet post der ikke findes")
@allure.description("Testdesign: Negativ test\nBeskrivelse: Forsøger at slette et post med et id der ikke eksisterer\nForventet: HTTP 200 — JSONPlaceholder returnerer 200 for alle DELETE requests")
def test_slet_post_der_ikke_findes():
    """
    Testdesign: Negativ test
    Beskrivelse: Forsøger at slette et post med et id der ikke eksisterer
    Forudsætning: Post med id 99999 eksisterer ikke i API'et
    Forventet resultat: HTTP 200 — JSONPlaceholder returnerer 200 for alle DELETE requests
    """
    response = delete("/posts/99999")
    print(f"\nResponse status: {response.status_code}")
    # JSONPlaceholder returnerer 200 selv for ikke-eksisterende ressourcer
    assert response.status_code == 200


@pytest.mark.regression
@allure.feature("Posts API")
@allure.story("DELETE")
@allure.title("Slet sidste gyldige post (id = 100)")
@allure.description("Testdesign: Grænseværdianalyse\nBeskrivelse: Sletter det sidste gyldige post ved øvre grænse (id = 100)\nForventet: HTTP 200")
def test_slet_sidste_gyldige_post():
    """
    Testdesign: Grænseværdianalyse
    Beskrivelse: Sletter det sidste gyldige post ved øvre grænse (id = 100)
    Forudsætning: API'et indeholder præcis 100 posts
    Forventet resultat: HTTP 200
    """
    response = delete("/posts/100")
    assert response.status_code == 200


@pytest.mark.regression
@allure.feature("Posts API")
@allure.story("DELETE")
@allure.title("Slet post med negativt id")
@allure.description("Testdesign: Grænseværdianalyse\nBeskrivelse: Forsøger at slette et post med negativt id (under nedre grænse)\nForventet: HTTP 200 — JSONPlaceholder validerer ikke id-værdier")
def test_slet_post_med_negativt_id():
    """
    Testdesign: Grænseværdianalyse
    Beskrivelse: Forsøger at slette et post med negativt id (under nedre grænse)
    Forudsætning: API'et er tilgængeligt
    Forventet resultat: HTTP 200 — JSONPlaceholder validerer ikke id-værdier
    """
    response = delete("/posts/-1")
    assert response.status_code == 200


@pytest.mark.regression
@allure.feature("Posts API")
@allure.story("DELETE")
@allure.title("Slet post med tekst som id")
@allure.description("Testdesign: Ækvivalenspartitionering\nBeskrivelse: Forsøger at slette et post med tekst som id (ugyldig partition)\nForventet: HTTP 200 — JSONPlaceholder validerer ikke id-typer")
def test_slet_post_med_tekst_som_id():
    """
    Testdesign: Ækvivalenspartitionering
    Beskrivelse: Forsøger at slette et post med tekst som id (ugyldig partition)
    Forudsætning: API'et er tilgængeligt
    Forventet resultat: HTTP 200 — JSONPlaceholder validerer ikke id-typer
    """
    response = delete("/posts/abc")
    assert response.status_code == 200


@pytest.mark.regression
@allure.feature("Posts API")
@allure.story("DELETE")
@allure.title("Valider tomt response ved DELETE")
@allure.description("Testdesign: Ækvivalenspartitionering\nBeskrivelse: Validerer at response ved DELETE er et tomt objekt\nForventet: HTTP 200 og response body er {}")
def test_valider_tomt_response():
    """
    Testdesign: Ækvivalenspartitionering
    Beskrivelse: Validerer at response ved DELETE er et tomt objekt
    Forudsætning: Post med id 1 eksisterer i API'et
    Forventet resultat: HTTP 200 og response body er {}
    """
    response = delete("/posts/1")
    assert response.status_code == 200
    assert response.json() == {}
