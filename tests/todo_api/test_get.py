import pytest
import allure
import requests
from tests.todo_api.conftest import BASE_URL
from api.models_db import TodoDB
from tests.todo_api.diagrams import (
    get_all_diagram,
    get_single_diagram,
    get_validate_fields_diagram,
    negative_get_diagram,
)
from tests.todo_api.testdesign_tables import get_equivalence_table

_REQS = {
    "REQ-003": "Completed skal være boolean (true/false)",
    "REQ-004": "ID genereres automatisk og er unikt og positivt",
    "REQ-005": "GET /todos returnerer HTTP 200 og liste med todos",
    "REQ-009": "Ugyldigt id returnerer HTTP 404",
    "REQ-012": "API'et skal svare inden for 2 sekunder",
    "REQ-013": "API'et skal understøtte HTTPS",
    "REQ-014": "API'et skal returnere JSON format",
    "REQ-015": "Databasen skal gemme data persistent",
}


def _link_reqs(*req_ids):
    for req_id in req_ids:
        allure.dynamic.link(f"#behaviors", name=f"{req_id}: {_REQS[req_id]}")


@pytest.mark.smoke
@pytest.mark.regression
@allure.feature("001_Tests")
@allure.story("001A_GET")
@allure.title("Hent alle todos")
@allure.description(
    "Beskrivelse: Henter alle todos fra /todos endpointet<br>"
    "Forventet: HTTP 200 og en liste med mindst én todo"
)
def test_hent_alle_todos(created_todo, db_session):
    """
    Testdesign: Ækvivalenspartitionering
    Beskrivelse: Henter alle todos fra /todos endpointet
    Forudsætning: API'et er tilgængeligt og indeholder mindst én todo
    Forventet resultat: HTTP 200 og en liste med mindst én todo
    """
    count_before = db_session.query(TodoDB).count()
    assert count_before > 0

    response = requests.get(f"{BASE_URL}/todos")
    print(f"\nResponse: {response.json()[:2]}")
    assert response.status_code == 200
    assert response.elapsed.total_seconds() < 2
    assert "application/json" in response.headers["Content-Type"]
    assert len(response.json()) > 0

    db_session.expire_all()
    count_after = db_session.query(TodoDB).count()
    assert count_after == count_before

    allure.attach(
        '<table border="1" style="border-collapse: collapse; width: 100%;">'
        '<tr style="background-color: #f2f2f2;"><th style="padding: 8px; text-align: left;">Assertion</th><th style="padding: 8px; text-align: left;">Forventet</th></tr>'
        '<tr><td style="padding: 8px;">count_before &gt; 0</td><td style="padding: 8px;">REQ-015: Data eksisterer i databasen</td></tr>'
        '<tr><td style="padding: 8px;">response.status_code == 200</td><td style="padding: 8px;">REQ-005: HTTP 200</td></tr>'
        '<tr><td style="padding: 8px;">response.elapsed.total_seconds() &lt; 2</td><td style="padding: 8px;">REQ-012: Svartid under 2 sekunder</td></tr>'
        '<tr><td style="padding: 8px;">"application/json" in Content-Type</td><td style="padding: 8px;">REQ-014: Response er JSON format</td></tr>'
        '<tr><td style="padding: 8px;">len(response.json()) &gt; 0</td><td style="padding: 8px;">REQ-005: Listen indeholder mindst én todo</td></tr>'
        '<tr><td style="padding: 8px;">count_after == count_before</td><td style="padding: 8px;">GET ændrede ikke antal rækker i databasen</td></tr>'
        "</table>",
        name="Database assertions",
        attachment_type=allure.attachment_type.HTML
    )
    allure.attach(get_equivalence_table("K1"), name="Testdesign", attachment_type=allure.attachment_type.HTML)
    allure.attach(get_all_diagram(), name="Flow Diagram", attachment_type=allure.attachment_type.HTML)
    _link_reqs("REQ-004", "REQ-005", "REQ-012", "REQ-013", "REQ-014", "REQ-015")


@pytest.mark.regression
@allure.feature("001_Tests")
@allure.story("001A_GET")
@allure.title("Hent enkelt todo med gyldigt id")
@allure.description(
    "Beskrivelse: Henter en enkelt todo med gyldigt id<br>"
    "Forventet: HTTP 200 og todo med korrekt id"
)
def test_hent_enkelt_todo(created_todo, db_session):
    """
    Testdesign: Ækvivalenspartitionering
    Beskrivelse: Henter en enkelt todo med gyldigt id
    Forudsætning: Todo eksisterer i API'et
    Forventet resultat: HTTP 200 og todo med korrekt id
    """
    todo_id = created_todo["id"]

    db_todo = db_session.query(TodoDB).filter_by(id=todo_id).first()
    assert db_todo is not None
    assert db_todo.id == todo_id
    assert db_todo.id > 0

    response = requests.get(f"{BASE_URL}/todos/{todo_id}")
    print(f"\nResponse: {response.json()}")
    assert response.status_code == 200
    assert response.elapsed.total_seconds() < 2
    assert "application/json" in response.headers["Content-Type"]
    assert response.json()["id"] == todo_id

    db_session.expire_all()
    db_todo_after = db_session.query(TodoDB).filter_by(id=todo_id).first()
    assert db_todo_after is not None
    assert db_todo_after.id == todo_id

    allure.attach(
        '<table border="1" style="border-collapse: collapse; width: 100%;">'
        '<tr style="background-color: #f2f2f2;"><th style="padding: 8px; text-align: left;">Assertion</th><th style="padding: 8px; text-align: left;">Forventet</th></tr>'
        '<tr><td style="padding: 8px;">db_todo is not None</td><td style="padding: 8px;">REQ-015: Todo eksisterer i databasen</td></tr>'
        '<tr><td style="padding: 8px;">db_todo.id == todo_id</td><td style="padding: 8px;">ID matcher det hentede todo</td></tr>'
        '<tr><td style="padding: 8px;">db_todo.id &gt; 0</td><td style="padding: 8px;">REQ-004: ID er positivt</td></tr>'
        '<tr><td style="padding: 8px;">response.status_code == 200</td><td style="padding: 8px;">REQ-005: HTTP 200</td></tr>'
        '<tr><td style="padding: 8px;">response.elapsed.total_seconds() &lt; 2</td><td style="padding: 8px;">REQ-012: Svartid under 2 sekunder</td></tr>'
        '<tr><td style="padding: 8px;">"application/json" in Content-Type</td><td style="padding: 8px;">REQ-014: Response er JSON format</td></tr>'
        '<tr><td style="padding: 8px;">response.json()["id"] == todo_id</td><td style="padding: 8px;">Response ID matcher</td></tr>'
        '<tr><td style="padding: 8px;">db_todo_after is not None</td><td style="padding: 8px;">Todo stadig i databasen efter GET</td></tr>'
        '<tr><td style="padding: 8px;">db_todo_after.id == todo_id</td><td style="padding: 8px;">Data er uændret af GET kaldet</td></tr>'
        "</table>",
        name="Database assertions",
        attachment_type=allure.attachment_type.HTML
    )
    allure.attach(get_equivalence_table("K2"), name="Testdesign", attachment_type=allure.attachment_type.HTML)
    allure.attach(get_single_diagram(todo_id), name="Flow Diagram", attachment_type=allure.attachment_type.HTML)
    _link_reqs("REQ-004", "REQ-005", "REQ-012", "REQ-013", "REQ-014", "REQ-015")


@pytest.mark.regression
@pytest.mark.negative
@allure.feature("001_Tests")
@allure.story("001A_GET")
@allure.title("Hent todo der ikke findes")
@allure.description("Beskrivelse: Forsøger at hente en todo med et id der ikke eksisterer\nForventet: HTTP 404")
def test_hent_todo_der_ikke_findes(db_session):
    """
    Testdesign: Negativ test
    Beskrivelse: Forsøger at hente en todo med et id der ikke eksisterer
    Forudsætning: Todo med id 99999 eksisterer ikke i API'et
    Forventet resultat: HTTP 404
    """
    db_todo = db_session.query(TodoDB).filter_by(id=99999).first()
    assert db_todo is None
    count_before = db_session.query(TodoDB).count()

    response = requests.get(f"{BASE_URL}/todos/99999")
    print(f"\nResponse: {response.status_code}")
    assert response.status_code == 404
    assert response.elapsed.total_seconds() < 2

    db_session.expire_all()
    count_after = db_session.query(TodoDB).count()
    assert count_after == count_before

    allure.attach(
        '<table border="1" style="border-collapse: collapse; width: 100%;">'
        '<tr style="background-color: #f2f2f2;"><th style="padding: 8px; text-align: left;">Assertion</th><th style="padding: 8px; text-align: left;">Forventet</th></tr>'
        '<tr><td style="padding: 8px;">db_todo is None</td><td style="padding: 8px;">ID 99999 eksisterer ikke i databasen</td></tr>'
        '<tr><td style="padding: 8px;">response.status_code == 404</td><td style="padding: 8px;">REQ-009: HTTP 404</td></tr>'
        '<tr><td style="padding: 8px;">response.elapsed.total_seconds() &lt; 2</td><td style="padding: 8px;">REQ-012: Svartid under 2 sekunder</td></tr>'
        '<tr><td style="padding: 8px;">count_after == count_before</td><td style="padding: 8px;">Antal rækker er uændret</td></tr>'
        "</table>",
        name="Database assertions",
        attachment_type=allure.attachment_type.HTML
    )
    allure.attach(get_equivalence_table("K4"), name="Testdesign", attachment_type=allure.attachment_type.HTML)
    allure.attach(negative_get_diagram(99999, 404), name="Flow Diagram", attachment_type=allure.attachment_type.HTML)
    _link_reqs("REQ-005", "REQ-009", "REQ-012", "REQ-013")


@pytest.mark.regression
@allure.feature("001_Tests")
@allure.story("001A_GET")
@allure.title("Valider felter i todo response")
@allure.description(
    "Beskrivelse: Validerer at en todo indeholder alle forventede felter<br>"
    "Forventet: HTTP 200 og response indeholder id, title, completed"
)
def test_valider_felter_i_todo(created_todo, db_session):
    """
    Testdesign: Ækvivalenspartitionering
    Beskrivelse: Validerer at en todo indeholder alle forventede felter
    Forudsætning: Todo eksisterer i API'et
    Forventet resultat: HTTP 200 og response indeholder felterne id, title, completed
    """
    todo_id = created_todo["id"]

    db_todo = db_session.query(TodoDB).filter_by(id=todo_id).first()
    assert db_todo is not None
    assert db_todo.id == todo_id
    assert db_todo.id > 0
    assert db_todo.title != ""
    assert isinstance(db_todo.completed, bool)

    response = requests.get(f"{BASE_URL}/todos/{todo_id}")
    todo = response.json()
    assert response.status_code == 200
    assert response.elapsed.total_seconds() < 2
    assert "application/json" in response.headers["Content-Type"]
    assert all(felt in todo for felt in ["id", "title", "completed"])

    db_session.expire_all()
    db_todo_after = db_session.query(TodoDB).filter_by(id=todo_id).first()
    assert db_todo_after is not None
    assert db_todo_after.id == todo_id
    assert db_todo_after.title != ""
    assert isinstance(db_todo_after.completed, bool)

    allure.attach(
        '<table border="1" style="border-collapse: collapse; width: 100%;">'
        '<tr style="background-color: #f2f2f2;"><th style="padding: 8px; text-align: left;">Assertion</th><th style="padding: 8px; text-align: left;">Forventet</th></tr>'
        '<tr><td style="padding: 8px;">db_todo is not None</td><td style="padding: 8px;">REQ-015: Todo eksisterer i databasen</td></tr>'
        '<tr><td style="padding: 8px;">db_todo.id &gt; 0</td><td style="padding: 8px;">REQ-004: ID er positivt</td></tr>'
        '<tr><td style="padding: 8px;">db_todo.title != ""</td><td style="padding: 8px;">Title er ikke tom</td></tr>'
        '<tr><td style="padding: 8px;">isinstance(db_todo.completed, bool)</td><td style="padding: 8px;">REQ-003: Completed er en boolean</td></tr>'
        '<tr><td style="padding: 8px;">response.status_code == 200</td><td style="padding: 8px;">REQ-005: HTTP 200</td></tr>'
        '<tr><td style="padding: 8px;">response.elapsed.total_seconds() &lt; 2</td><td style="padding: 8px;">REQ-012: Svartid under 2 sekunder</td></tr>'
        '<tr><td style="padding: 8px;">"application/json" in Content-Type</td><td style="padding: 8px;">REQ-014: Response er JSON format</td></tr>'
        '<tr><td style="padding: 8px;">all(felt in todo for felt in [...])</td><td style="padding: 8px;">Response indeholder id, title, completed</td></tr>'
        '<tr><td style="padding: 8px;">db_todo_after is not None</td><td style="padding: 8px;">Todo stadig i databasen efter GET</td></tr>'
        '<tr><td style="padding: 8px;">db_todo_after.id == todo_id</td><td style="padding: 8px;">Data er uændret af GET kaldet</td></tr>'
        "</table>",
        name="Database assertions",
        attachment_type=allure.attachment_type.HTML
    )
    allure.attach(get_equivalence_table("K3"), name="Testdesign", attachment_type=allure.attachment_type.HTML)
    allure.attach(get_validate_fields_diagram(todo_id), name="Flow Diagram", attachment_type=allure.attachment_type.HTML)
    _link_reqs("REQ-003", "REQ-004", "REQ-005", "REQ-012", "REQ-013", "REQ-014", "REQ-015")


@pytest.mark.regression
@pytest.mark.negative
@allure.feature("001_Tests")
@allure.story("001A_GET")
@allure.title("Hent todo med negativt id")
@allure.description("Beskrivelse: Forsøger at hente en todo med negativt id (under nedre grænse)\nForventet: HTTP 404")
def test_hent_todo_med_negativt_id(db_session):
    """
    Testdesign: Grænseværdianalyse
    Beskrivelse: Forsøger at hente en todo med negativt id (under nedre grænse)
    Forudsætning: API'et accepterer ikke negative id-værdier
    Forventet resultat: HTTP 404
    """
    db_todo = db_session.query(TodoDB).filter_by(id=-1).first()
    assert db_todo is None
    count_before = db_session.query(TodoDB).count()

    response = requests.get(f"{BASE_URL}/todos/-1")
    assert response.status_code == 404
    assert response.elapsed.total_seconds() < 2

    db_session.expire_all()
    count_after = db_session.query(TodoDB).count()
    assert count_after == count_before

    allure.attach(
        '<table border="1" style="border-collapse: collapse; width: 100%;">'
        '<tr style="background-color: #f2f2f2;"><th style="padding: 8px; text-align: left;">Assertion</th><th style="padding: 8px; text-align: left;">Forventet</th></tr>'
        '<tr><td style="padding: 8px;">db_todo is None</td><td style="padding: 8px;">ID -1 eksisterer ikke i databasen</td></tr>'
        '<tr><td style="padding: 8px;">response.status_code == 404</td><td style="padding: 8px;">REQ-009: HTTP 404</td></tr>'
        '<tr><td style="padding: 8px;">response.elapsed.total_seconds() &lt; 2</td><td style="padding: 8px;">REQ-012: Svartid under 2 sekunder</td></tr>'
        '<tr><td style="padding: 8px;">count_after == count_before</td><td style="padding: 8px;">Antal rækker er uændret</td></tr>'
        "</table>",
        name="Database assertions",
        attachment_type=allure.attachment_type.HTML
    )
    allure.attach(get_equivalence_table("K5"), name="Testdesign", attachment_type=allure.attachment_type.HTML)
    allure.attach(negative_get_diagram(-1, 404), name="Flow Diagram", attachment_type=allure.attachment_type.HTML)
    _link_reqs("REQ-005", "REQ-009", "REQ-012", "REQ-013")


@pytest.mark.regression
@pytest.mark.negative
@allure.feature("001_Tests")
@allure.story("001A_GET")
@allure.title("Hent todo med ugyldigt id (tekst)")
@allure.description("Beskrivelse: Forsøger at hente en todo med tekst som id (ugyldig partition)\nForventet: HTTP 422")
def test_hent_todo_med_ugyldigt_id(db_session):
    """
    Testdesign: Ækvivalenspartitionering
    Beskrivelse: Forsøger at hente en todo med tekst som id (ugyldig partition)
    Forudsætning: API'et forventer numeriske id-værdier
    Forventet resultat: HTTP 422 (FastAPI validering)
    """
    count_before = db_session.query(TodoDB).count()

    response = requests.get(f"{BASE_URL}/todos/abc")
    assert response.status_code == 422
    assert response.elapsed.total_seconds() < 2

    db_session.expire_all()
    count_after = db_session.query(TodoDB).count()
    assert count_after == count_before

    allure.attach(
        '<table border="1" style="border-collapse: collapse; width: 100%;">'
        '<tr style="background-color: #f2f2f2;"><th style="padding: 8px; text-align: left;">Assertion</th><th style="padding: 8px; text-align: left;">Forventet</th></tr>'
        '<tr><td style="padding: 8px;">count_before (baseline)</td><td style="padding: 8px;">Registrerer antal rækker inden kaldet</td></tr>'
        '<tr><td style="padding: 8px;">response.status_code == 422</td><td style="padding: 8px;">HTTP 422 (FastAPI validerer id-typen)</td></tr>'
        '<tr><td style="padding: 8px;">response.elapsed.total_seconds() &lt; 2</td><td style="padding: 8px;">REQ-012: Svartid under 2 sekunder</td></tr>'
        '<tr><td style="padding: 8px;">count_after == count_before</td><td style="padding: 8px;">Antal rækker er uændret</td></tr>'
        "</table>",
        name="Database assertions",
        attachment_type=allure.attachment_type.HTML
    )
    allure.attach(get_equivalence_table("K6"), name="Testdesign", attachment_type=allure.attachment_type.HTML)
    allure.attach(negative_get_diagram("abc", 422), name="Flow Diagram", attachment_type=allure.attachment_type.HTML)
    _link_reqs("REQ-005", "REQ-012", "REQ-013")
