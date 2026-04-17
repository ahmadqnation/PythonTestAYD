import pytest
import allure
import requests
from tests.todo_api.conftest import BASE_URL
from api.models_db import TodoDB
from tests.todo_api.diagrams import put_diagram, negative_put_diagram
from tests.todo_api.testdesign_tables import put_equivalence_table

_REQS = {
    "REQ-003": "Completed skal være boolean (true/false)",
    "REQ-004": "ID genereres automatisk og er unikt og positivt",
    "REQ-007": "PUT /todos/{id} returnerer HTTP 200 og opdaterer todo",
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
@allure.story("001C_PUT")
@allure.title("Opdater todo titel")
@allure.description(
    "Beskrivelse: Opdaterer titlen på en eksisterende todo<br>"
    "Forventet: HTTP 200 og titel matcher den sendte værdi"
)
def test_opdater_todo_titel(created_todo, db_session, auth_headers):
    """
    Testdesign: Ækvivalenspartitionering
    Beskrivelse: Opdaterer titlen på en eksisterende todo
    Forudsætning: Todo eksisterer i API'et
    Forventet resultat: HTTP 200 og titel matcher den sendte værdi
    """
    todo_id = created_todo["id"]
    response = requests.put(f"{BASE_URL}/todos/{todo_id}", json={"title": "Opdateret titel"}, headers=auth_headers)
    print(f"\nResponse: {response.json()}")
    assert response.status_code == 200
    assert response.elapsed.total_seconds() < 2
    assert "application/json" in response.headers["Content-Type"]
    assert response.json()["title"] == "Opdateret titel"

    db_todo = db_session.query(TodoDB).filter_by(id=todo_id).first()
    assert db_todo is not None
    assert db_todo.id == todo_id
    assert db_todo.id > 0
    assert db_todo.title == "Opdateret titel"
    assert db_todo.title != ""
    assert db_todo.completed == False
    assert isinstance(db_todo.completed, bool)

    allure.attach(
        '<table border="1" style="border-collapse: collapse; width: 100%;">'
        '<tr style="background-color: #f2f2f2;"><th style="padding: 8px; text-align: left;">Assertion</th><th style="padding: 8px; text-align: left;">Forventet</th></tr>'
        '<tr><td style="padding: 8px;">response.elapsed.total_seconds() &lt; 2</td><td style="padding: 8px;">REQ-012: Svartid under 2 sekunder</td></tr>'
        '<tr><td style="padding: 8px;">"application/json" in Content-Type</td><td style="padding: 8px;">REQ-014: Response er JSON format</td></tr>'
        '<tr><td style="padding: 8px;">db_todo is not None</td><td style="padding: 8px;">REQ-015: Rækken eksisterer i databasen</td></tr>'
        '<tr><td style="padding: 8px;">db_todo.id == todo_id</td><td style="padding: 8px;">ID matcher det opdaterede todo</td></tr>'
        '<tr><td style="padding: 8px;">db_todo.id &gt; 0</td><td style="padding: 8px;">REQ-004: ID er positivt</td></tr>'
        '<tr><td style="padding: 8px;">db_todo.title == "Opdateret titel"</td><td style="padding: 8px;">REQ-007: Title er korrekt opdateret i databasen</td></tr>'
        '<tr><td style="padding: 8px;">db_todo.title != ""</td><td style="padding: 8px;">Title er ikke tom</td></tr>'
        '<tr><td style="padding: 8px;">db_todo.completed == False</td><td style="padding: 8px;">Completed er uændret (False)</td></tr>'
        '<tr><td style="padding: 8px;">isinstance(completed, bool)</td><td style="padding: 8px;">REQ-003: Completed er en boolean</td></tr>'
        "</table>",
        name="Database assertions",
        attachment_type=allure.attachment_type.HTML
    )
    allure.attach(put_equivalence_table("K1"), name="Testdesign", attachment_type=allure.attachment_type.HTML)
    allure.attach(put_diagram("Opdateret titel", False), name="Flow Diagram", attachment_type=allure.attachment_type.HTML)
    _link_reqs("REQ-003", "REQ-004", "REQ-007", "REQ-012", "REQ-013", "REQ-014", "REQ-015")


@pytest.mark.regression
@allure.feature("001_Tests")
@allure.story("001C_PUT")
@allure.title("Opdater todo completed status")
@allure.description(
    "Beskrivelse: Opdaterer completed-feltet på en eksisterende todo<br>"
    "Forventet: HTTP 200 og completed = true"
)
def test_opdater_todo_completed(created_todo, db_session, auth_headers):
    """
    Testdesign: Ækvivalenspartitionering
    Beskrivelse: Opdaterer completed-feltet på en eksisterende todo
    Forudsætning: Todo eksisterer i API'et med completed = false
    Forventet resultat: HTTP 200 og completed = true
    """
    todo_id = created_todo["id"]
    response = requests.put(f"{BASE_URL}/todos/{todo_id}", json={"completed": True}, headers=auth_headers)
    assert response.status_code == 200
    assert response.elapsed.total_seconds() < 2
    assert "application/json" in response.headers["Content-Type"]
    assert response.json()["completed"] is True

    db_todo = db_session.query(TodoDB).filter_by(id=todo_id).first()
    assert db_todo is not None
    assert db_todo.id == todo_id
    assert db_todo.id > 0
    assert db_todo.title == created_todo["title"]
    assert db_todo.title != ""
    assert db_todo.completed == True
    assert isinstance(db_todo.completed, bool)

    allure.attach(
        '<table border="1" style="border-collapse: collapse; width: 100%;">'
        '<tr style="background-color: #f2f2f2;"><th style="padding: 8px; text-align: left;">Assertion</th><th style="padding: 8px; text-align: left;">Forventet</th></tr>'
        '<tr><td style="padding: 8px;">response.elapsed.total_seconds() &lt; 2</td><td style="padding: 8px;">REQ-012: Svartid under 2 sekunder</td></tr>'
        '<tr><td style="padding: 8px;">"application/json" in Content-Type</td><td style="padding: 8px;">REQ-014: Response er JSON format</td></tr>'
        '<tr><td style="padding: 8px;">db_todo is not None</td><td style="padding: 8px;">REQ-015: Rækken eksisterer i databasen</td></tr>'
        '<tr><td style="padding: 8px;">db_todo.id == todo_id</td><td style="padding: 8px;">ID matcher det opdaterede todo</td></tr>'
        '<tr><td style="padding: 8px;">db_todo.id &gt; 0</td><td style="padding: 8px;">REQ-004: ID er positivt</td></tr>'
        '<tr><td style="padding: 8px;">db_todo.title == created_todo["title"]</td><td style="padding: 8px;">Title er uændret i databasen</td></tr>'
        '<tr><td style="padding: 8px;">db_todo.title != ""</td><td style="padding: 8px;">Title er ikke tom</td></tr>'
        '<tr><td style="padding: 8px;">db_todo.completed == True</td><td style="padding: 8px;">REQ-003/REQ-007: Completed er korrekt opdateret til True</td></tr>'
        '<tr><td style="padding: 8px;">isinstance(completed, bool)</td><td style="padding: 8px;">REQ-003: Completed er en boolean</td></tr>'
        "</table>",
        name="Database assertions",
        attachment_type=allure.attachment_type.HTML
    )
    allure.attach(put_equivalence_table("K2"), name="Testdesign", attachment_type=allure.attachment_type.HTML)
    allure.attach(put_diagram(created_todo["title"], True), name="Flow Diagram", attachment_type=allure.attachment_type.HTML)
    _link_reqs("REQ-003", "REQ-004", "REQ-007", "REQ-012", "REQ-013", "REQ-014", "REQ-015")


@pytest.mark.regression
@pytest.mark.negative
@allure.feature("001_Tests")
@allure.story("001C_PUT")
@allure.title("Opdater todo der ikke findes")
@allure.description("Beskrivelse: Forsøger at opdatere en todo med et id der ikke eksisterer\nForventet: HTTP 404")
def test_opdater_todo_der_ikke_findes(db_session, auth_headers):
    """
    Testdesign: Negativ test
    Beskrivelse: Forsøger at opdatere en todo med et id der ikke eksisterer
    Forudsætning: Todo med id 99999 eksisterer ikke i API'et
    Forventet resultat: HTTP 404
    """
    db_todo = db_session.query(TodoDB).filter_by(id=99999).first()
    assert db_todo is None

    response = requests.put(f"{BASE_URL}/todos/99999", json={"title": "Findes ikke"}, headers=auth_headers)
    print(f"\nResponse status: {response.status_code}")
    assert response.status_code == 404
    assert response.elapsed.total_seconds() < 2

    allure.attach(
        '<table border="1" style="border-collapse: collapse; width: 100%;">'
        '<tr style="background-color: #f2f2f2;"><th style="padding: 8px; text-align: left;">Assertion</th><th style="padding: 8px; text-align: left;">Forventet</th></tr>'
        '<tr><td style="padding: 8px;">db_todo is None</td><td style="padding: 8px;">ID 99999 eksisterer ikke i databasen</td></tr>'
        '<tr><td style="padding: 8px;">response.status_code == 404</td><td style="padding: 8px;">REQ-009: HTTP 404</td></tr>'
        '<tr><td style="padding: 8px;">response.elapsed.total_seconds() &lt; 2</td><td style="padding: 8px;">REQ-012: Svartid under 2 sekunder</td></tr>'
        "</table>",
        name="Database assertions",
        attachment_type=allure.attachment_type.HTML
    )
    allure.attach(put_equivalence_table("K4"), name="Testdesign", attachment_type=allure.attachment_type.HTML)
    allure.attach(negative_put_diagram(99999), name="Flow Diagram", attachment_type=allure.attachment_type.HTML)
    _link_reqs("REQ-007", "REQ-009", "REQ-012", "REQ-013")


@pytest.mark.regression
@allure.feature("001_Tests")
@allure.story("001C_PUT")
@allure.title("Opdater todo med tomt objekt")
@allure.description(
    "Beskrivelse: Opdaterer en todo med et tomt objekt<br>"
    "Forventet: HTTP 200 og todo er uændret"
)
def test_opdater_todo_med_tomt_objekt(created_todo, db_session, auth_headers):
    """
    Testdesign: Ækvivalenspartitionering
    Beskrivelse: Opdaterer en todo med et tomt objekt (ingen felter ændres)
    Forudsætning: Todo eksisterer i API'et
    Forventet resultat: HTTP 200 og todo er uændret
    """
    todo_id = created_todo["id"]
    response = requests.put(f"{BASE_URL}/todos/{todo_id}", json={}, headers=auth_headers)
    assert response.status_code == 200
    assert response.elapsed.total_seconds() < 2
    assert response.json()["title"] == created_todo["title"]

    db_todo = db_session.query(TodoDB).filter_by(id=todo_id).first()
    assert db_todo is not None
    assert db_todo.id == todo_id
    assert db_todo.id > 0
    assert db_todo.title == created_todo["title"]
    assert db_todo.title != ""
    assert db_todo.completed == created_todo["completed"]
    assert isinstance(db_todo.completed, bool)

    allure.attach(
        '<table border="1" style="border-collapse: collapse; width: 100%;">'
        '<tr style="background-color: #f2f2f2;"><th style="padding: 8px; text-align: left;">Assertion</th><th style="padding: 8px; text-align: left;">Forventet</th></tr>'
        '<tr><td style="padding: 8px;">response.elapsed.total_seconds() &lt; 2</td><td style="padding: 8px;">REQ-012: Svartid under 2 sekunder</td></tr>'
        '<tr><td style="padding: 8px;">db_todo is not None</td><td style="padding: 8px;">REQ-015: Rækken eksisterer i databasen</td></tr>'
        '<tr><td style="padding: 8px;">db_todo.id == todo_id</td><td style="padding: 8px;">ID matcher det opdaterede todo</td></tr>'
        '<tr><td style="padding: 8px;">db_todo.id &gt; 0</td><td style="padding: 8px;">REQ-004: ID er positivt</td></tr>'
        '<tr><td style="padding: 8px;">db_todo.title == created_todo["title"]</td><td style="padding: 8px;">REQ-007: Title er uændret i databasen</td></tr>'
        '<tr><td style="padding: 8px;">db_todo.title != ""</td><td style="padding: 8px;">Title er ikke tom</td></tr>'
        '<tr><td style="padding: 8px;">db_todo.completed == created_todo["completed"]</td><td style="padding: 8px;">Completed er uændret i databasen</td></tr>'
        '<tr><td style="padding: 8px;">isinstance(completed, bool)</td><td style="padding: 8px;">REQ-003: Completed er en boolean</td></tr>'
        "</table>",
        name="Database assertions",
        attachment_type=allure.attachment_type.HTML
    )
    allure.attach(put_equivalence_table("K3"), name="Testdesign", attachment_type=allure.attachment_type.HTML)
    allure.attach(put_diagram(created_todo["title"], created_todo["completed"]), name="Flow Diagram", attachment_type=allure.attachment_type.HTML)
    _link_reqs("REQ-003", "REQ-004", "REQ-007", "REQ-012", "REQ-013", "REQ-015")


@pytest.mark.regression
@allure.feature("001_Tests")
@allure.story("001C_PUT")
@allure.title("Valider felter i PUT response")
@allure.description(
    "Beskrivelse: Validerer at response indeholder alle forventede felter efter opdatering<br>"
    "Forventet: HTTP 200 og response indeholder id, title, completed"
)
def test_valider_felter_i_response(created_todo, db_session, auth_headers):
    """
    Testdesign: Ækvivalenspartitionering
    Beskrivelse: Validerer at response indeholder alle forventede felter efter opdatering
    Forudsætning: Todo eksisterer i API'et
    Forventet resultat: HTTP 200 og response indeholder felterne id, title, completed
    """
    todo_id = created_todo["id"]
    response = requests.put(f"{BASE_URL}/todos/{todo_id}", json={"title": "Opdateret"}, headers=auth_headers)
    todo = response.json()
    assert response.status_code == 200
    assert response.elapsed.total_seconds() < 2
    assert all(felt in todo for felt in ["id", "title", "completed"])

    db_todo = db_session.query(TodoDB).filter_by(id=todo_id).first()
    assert db_todo is not None
    assert db_todo.id == todo_id
    assert db_todo.id > 0
    assert db_todo.title == "Opdateret"
    assert db_todo.title != ""
    assert db_todo.completed == False
    assert isinstance(db_todo.completed, bool)

    allure.attach(
        '<table border="1" style="border-collapse: collapse; width: 100%;">'
        '<tr style="background-color: #f2f2f2;"><th style="padding: 8px; text-align: left;">Assertion</th><th style="padding: 8px; text-align: left;">Forventet</th></tr>'
        '<tr><td style="padding: 8px;">response.elapsed.total_seconds() &lt; 2</td><td style="padding: 8px;">REQ-012: Svartid under 2 sekunder</td></tr>'
        '<tr><td style="padding: 8px;">db_todo is not None</td><td style="padding: 8px;">REQ-015: Rækken eksisterer i databasen</td></tr>'
        '<tr><td style="padding: 8px;">db_todo.id == todo_id</td><td style="padding: 8px;">ID matcher det opdaterede todo</td></tr>'
        '<tr><td style="padding: 8px;">db_todo.id &gt; 0</td><td style="padding: 8px;">REQ-004: ID er positivt</td></tr>'
        '<tr><td style="padding: 8px;">db_todo.title == "Opdateret"</td><td style="padding: 8px;">REQ-007: Title er korrekt opdateret i databasen</td></tr>'
        '<tr><td style="padding: 8px;">db_todo.title != ""</td><td style="padding: 8px;">Title er ikke tom</td></tr>'
        '<tr><td style="padding: 8px;">db_todo.completed == False</td><td style="padding: 8px;">Completed er uændret (False)</td></tr>'
        '<tr><td style="padding: 8px;">isinstance(completed, bool)</td><td style="padding: 8px;">REQ-003: Completed er en boolean</td></tr>'
        "</table>",
        name="Database assertions",
        attachment_type=allure.attachment_type.HTML
    )
    allure.attach(put_equivalence_table("K1"), name="Testdesign", attachment_type=allure.attachment_type.HTML)
    allure.attach(put_diagram("Opdateret", False), name="Flow Diagram", attachment_type=allure.attachment_type.HTML)
    _link_reqs("REQ-003", "REQ-004", "REQ-007", "REQ-012", "REQ-013", "REQ-015")
