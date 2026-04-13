import pytest
import allure
from helpers.api_client import get


@pytest.mark.smoke
@pytest.mark.regression
@allure.feature("Comments API")
@allure.story("GET")
@allure.title("Hent alle comments")
@allure.description("Testdesign: Ækvivalenspartitionering\nBeskrivelse: Henter alle comments fra /comments endpointet\nForventet: HTTP 200 og en liste med mindst én kommentar")
def test_hent_alle_comments():
    """
    Testdesign: Ækvivalenspartitionering
    Beskrivelse: Henter alle comments fra /comments endpointet
    Forudsætning: API'et er tilgængeligt og indeholder comments
    Forventet resultat: HTTP 200 og en liste med mindst én kommentar
    """
    response = get("/comments")
    print(f"\nResponse: {response.json()[:2]}")
    assert response.status_code == 200
    assert len(response.json()) > 0


@pytest.mark.regression
@allure.feature("Comments API")
@allure.story("GET")
@allure.title("Hent enkelt comment med gyldigt id")
@allure.description("Testdesign: Ækvivalenspartitionering\nBeskrivelse: Henter en enkelt comment med gyldigt id\nForventet: HTTP 200 og comment med id = 1")
def test_hent_enkelt_comment():
    """
    Testdesign: Ækvivalenspartitionering
    Beskrivelse: Henter en enkelt comment med gyldigt id
    Forudsætning: Comment med id 1 eksisterer i API'et
    Forventet resultat: HTTP 200 og en comment med id = 1
    """
    response = get("/comments/1")
    print(f"\nResponse: {response.json()}")
    assert response.status_code == 200
    assert response.json()["id"] == 1


@pytest.mark.regression
@pytest.mark.negative
@allure.feature("Comments API")
@allure.story("GET")
@allure.title("Hent comment der ikke findes")
@allure.description("Testdesign: Negativ test\nBeskrivelse: Forsøger at hente en comment med et id der ikke eksisterer\nForventet: HTTP 404")
def test_hent_comment_der_ikke_findes():
    """
    Testdesign: Negativ test
    Beskrivelse: Forsøger at hente en comment med et id der ikke eksisterer
    Forudsætning: Comment med id 99999 eksisterer ikke i API'et
    Forventet resultat: HTTP 404
    """
    response = get("/comments/99999")
    print(f"\nResponse: {response.status_code}")
    assert response.status_code == 404


@pytest.mark.regression
@allure.feature("Comments API")
@allure.story("GET")
@allure.title("Hent sidste gyldige comment (id = 500)")
@allure.description("Testdesign: Grænseværdianalyse\nBeskrivelse: Henter den sidste gyldige comment ved øvre grænse (id = 500)\nForventet: HTTP 200")
def test_hent_sidste_gyldige_comment():
    """
    Testdesign: Grænseværdianalyse
    Beskrivelse: Henter den sidste gyldige comment ved øvre grænse (id = 500)
    Forudsætning: API'et indeholder præcis 500 comments
    Forventet resultat: HTTP 200
    """
    response = get("/comments/500")
    assert response.status_code == 200


@pytest.mark.regression
@pytest.mark.negative
@allure.feature("Comments API")
@allure.story("GET")
@allure.title("Hent comment med negativt id")
@allure.description("Testdesign: Grænseværdianalyse\nBeskrivelse: Forsøger at hente en comment med negativt id (under nedre grænse)\nForventet: HTTP 404")
def test_hent_comment_med_negativt_id():
    """
    Testdesign: Grænseværdianalyse
    Beskrivelse: Forsøger at hente en comment med negativt id (under nedre grænse)
    Forudsætning: API'et accepterer ikke negative id-værdier
    Forventet resultat: HTTP 404
    """
    response = get("/comments/-1")
    assert response.status_code == 404


@pytest.mark.regression
@pytest.mark.negative
@allure.feature("Comments API")
@allure.story("GET")
@allure.title("Hent comment med tekst som id")
@allure.description("Testdesign: Ækvivalenspartitionering\nBeskrivelse: Forsøger at hente en comment med tekst som id (ugyldig partition)\nForventet: HTTP 404")
def test_hent_comment_med_tekst_som_id():
    """
    Testdesign: Ækvivalenspartitionering
    Beskrivelse: Forsøger at hente en comment med tekst som id (ugyldig partition)
    Forudsætning: API'et forventer numeriske id-værdier
    Forventet resultat: HTTP 404
    """
    response = get("/comments/abc")
    assert response.status_code == 404


@pytest.mark.regression
@allure.feature("Comments API")
@allure.story("GET")
@allure.title("Valider felter i comment response")
@allure.description("Testdesign: Ækvivalenspartitionering\nBeskrivelse: Validerer at en comment indeholder alle forventede felter\nForventet: HTTP 200 og response indeholder id, postId, name, email, body")
def test_valider_felter_i_comment():
    """
    Testdesign: Ækvivalenspartitionering
    Beskrivelse: Validerer at en comment indeholder alle forventede felter
    Forudsætning: Comment med id 1 eksisterer i API'et
    Forventet resultat: HTTP 200 og response indeholder felterne id, postId, name, email, body
    """
    response = get("/comments/1")
    comment = response.json()
    assert response.status_code == 200
    assert all(felt in comment for felt in ["id", "postId", "name", "email", "body"])


@pytest.mark.regression
@allure.feature("Comments API")
@allure.story("GET")
@allure.title("Hent comments for et post")
@allure.description("Testdesign: Ækvivalenspartitionering\nBeskrivelse: Henter comments tilknyttet et gyldigt post\nForventet: HTTP 200 og mindst én kommentar")
def test_hent_comments_for_post():
    """
    Testdesign: Ækvivalenspartitionering
    Beskrivelse: Henter comments tilknyttet et gyldigt post
    Forudsætning: Post med id 1 eksisterer og har comments
    Forventet resultat: HTTP 200 og mindst én kommentar
    """
    response = get("/posts/1/comments")
    print(f"\nResponse: {response.json()[:2]}")
    assert response.status_code == 200
    assert len(response.json()) > 0
