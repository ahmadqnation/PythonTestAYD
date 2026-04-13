import pytest
import allure
from helpers.api_client import get


@pytest.mark.smoke
@pytest.mark.regression
@allure.feature("Posts API")
@allure.story("GET")
@allure.title("Hent alle posts")
@allure.description("Testdesign: Ækvivalenspartitionering\nBeskrivelse: Henter alle posts fra /posts endpointet\nForventet: HTTP 200 og en liste med mindst ét post")
def test_hent_alle_posts():
    """
    Testdesign: Ækvivalenspartitionering
    Beskrivelse: Henter alle posts fra /posts endpointet
    Forudsætning: API'et er tilgængeligt og indeholder posts
    Forventet resultat: HTTP 200 og en liste med mindst ét post
    """
    response = get("/posts")
    print(f"\nResponse: {response.json()[:2]}")
    assert response.status_code == 200
    assert len(response.json()) > 0


@pytest.mark.regression
@allure.feature("Posts API")
@allure.story("GET")
@allure.title("Hent enkelt post med gyldigt id")
@allure.description("Testdesign: Ækvivalenspartitionering\nBeskrivelse: Henter et enkelt post med gyldigt id\nForventet: HTTP 200 og post med id = 1")
def test_hent_enkelt_post():
    """
    Testdesign: Ækvivalenspartitionering
    Beskrivelse: Henter et enkelt post med gyldigt id
    Forudsætning: Post med id 1 eksisterer i API'et
    Forventet resultat: HTTP 200 og et post med id = 1
    """
    response = get("/posts/1")
    print(f"\nResponse: {response.json()}")
    assert response.status_code == 200
    assert response.json()["id"] == 1


@pytest.mark.regression
@pytest.mark.negative
@allure.feature("Posts API")
@allure.story("GET")
@allure.title("Hent post der ikke findes")
@allure.description("Testdesign: Negativ test\nBeskrivelse: Forsøger at hente et post med et id der ikke eksisterer\nForventet: HTTP 404")
def test_hent_post_der_ikke_findes():
    """
    Testdesign: Negativ test
    Beskrivelse: Forsøger at hente et post med et id der ikke eksisterer
    Forudsætning: Post med id 99999 eksisterer ikke i API'et
    Forventet resultat: HTTP 404
    """
    response = get("/posts/99999")
    print(f"\nResponse: {response.status_code}")
    assert response.status_code == 404


@pytest.mark.regression
@allure.feature("Posts API")
@allure.story("GET")
@allure.title("Hent kommentarer til et post")
@allure.description("Testdesign: Ækvivalenspartitionering\nBeskrivelse: Henter kommentarer tilknyttet et gyldigt post\nForventet: HTTP 200, mindst én kommentar med feltet email")
def test_hent_comments_til_post():
    """
    Testdesign: Ækvivalenspartitionering
    Beskrivelse: Henter kommentarer tilknyttet et gyldigt post
    Forudsætning: Post med id 1 eksisterer og har kommentarer
    Forventet resultat: HTTP 200, mindst én kommentar med feltet email
    """
    response = get("/posts/1/comments")
    print(f"\nResponse: {response.json()[:2]}")
    assert response.status_code == 200
    assert len(response.json()) > 0
    assert "email" in response.json()[0]


@pytest.mark.regression
@allure.feature("Posts API")
@allure.story("GET")
@allure.title("Hent sidste gyldige post (id = 100)")
@allure.description("Testdesign: Grænseværdianalyse\nBeskrivelse: Henter det sidste gyldige post ved øvre grænse (id = 100)\nForventet: HTTP 200")
def test_hent_sidste_gyldige_post():
    """
    Testdesign: Grænseværdianalyse
    Beskrivelse: Henter det sidste gyldige post ved øvre grænse (id = 100)
    Forudsætning: API'et indeholder præcis 100 posts
    Forventet resultat: HTTP 200
    """
    response = get("/posts/100")
    assert response.status_code == 200


@pytest.mark.regression
@pytest.mark.negative
@allure.feature("Posts API")
@allure.story("GET")
@allure.title("Hent post med negativt id")
@allure.description("Testdesign: Grænseværdianalyse\nBeskrivelse: Forsøger at hente et post med negativt id (under nedre grænse)\nForventet: HTTP 404")
def test_hent_post_med_negativt_id():
    """
    Testdesign: Grænseværdianalyse
    Beskrivelse: Forsøger at hente et post med negativt id (under nedre grænse)
    Forudsætning: API'et accepterer ikke negative id-værdier
    Forventet resultat: HTTP 404
    """
    response = get("/posts/-1")
    assert response.status_code == 404


@pytest.mark.regression
@pytest.mark.negative
@allure.feature("Posts API")
@allure.story("GET")
@allure.title("Hent post med tekst som id")
@allure.description("Testdesign: Ækvivalenspartitionering\nBeskrivelse: Forsøger at hente et post med tekst som id (ugyldig partition)\nForventet: HTTP 404")
def test_hent_post_med_tekst_som_id():
    """
    Testdesign: Ækvivalenspartitionering
    Beskrivelse: Forsøger at hente et post med tekst som id (ugyldig partition)
    Forudsætning: API'et forventer numeriske id-værdier
    Forventet resultat: HTTP 404
    """
    response = get("/posts/abc")
    assert response.status_code == 404


@pytest.mark.regression
@allure.feature("Posts API")
@allure.story("GET")
@allure.title("Valider felter i post response")
@allure.description("Testdesign: Ækvivalenspartitionering\nBeskrivelse: Validerer at et post indeholder alle forventede felter\nForventet: HTTP 200 og response indeholder id, userId, title, body")
def test_valider_felter_i_post():
    """
    Testdesign: Ækvivalenspartitionering
    Beskrivelse: Validerer at et post indeholder alle forventede felter
    Forudsætning: Post med id 1 eksisterer i API'et
    Forventet resultat: HTTP 200 og response indeholder felterne id, userId, title, body
    """
    response = get("/posts/1")
    post = response.json()
    assert response.status_code == 200
    assert all(felt in post for felt in ["id", "userId", "title", "body"])
