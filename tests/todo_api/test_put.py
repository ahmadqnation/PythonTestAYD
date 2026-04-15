import pytest
import allure
import requests
from tests.todo_api.conftest import BASE_URL
from api.models_db import TodoDB
from tests.todo_api.diagrams import put_diagram, negative_put_diagram


@pytest.mark.smoke
@pytest.mark.regression
@allure.feature("Todo API")
@allure.story("PUT")
@allure.title("Opdater todo titel")
@allure.description(
    "Testdesign: Ækvivalenspartitionering<br>"
    "Beskrivelse: Opdaterer titlen på en eksisterende todo<br>"
    "Forventet: HTTP 200 og titel matcher den sendte værdi"
)
def test_opdater_todo_titel(created_todo, db_session):
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
        '<tr><td style="padding: 8px;">db_todo is not None</td><td style="padding: 8px;">Rækken eksisterer i databasen</td></tr>'
        '<tr><td style="padding: 8px;">db_todo.id == todo_id</td><td style="padding: 8px;">ID matcher det opdaterede todo</td></tr>'
        '<tr><td style="padding: 8px;">db_todo.id > 0</td><td style="padding: 8px;">ID er positivt</td></tr>'
        '<tr><td style="padding: 8px;">db_todo.title == "Opdateret titel"</td><td style="padding: 8px;">Title er korrekt opdateret i databasen</td></tr>'
        '<tr><td style="padding: 8px;">db_todo.title != ""</td><td style="padding: 8px;">Title er ikke tom</td></tr>'
        '<tr><td style="padding: 8px;">db_todo.completed == False</td><td style="padding: 8px;">Completed er uændret (False)</td></tr>'
        '<tr><td style="padding: 8px;">isinstance(completed, bool)</td><td style="padding: 8px;">Completed er en boolean</td></tr>'
        "</table>",
        name="Database assertions",
        attachment_type=allure.attachment_type.HTML
    )

    allure.attach(put_diagram("Opdateret titel", False), name="Flow Diagram", attachment_type=allure.attachment_type.HTML)


@pytest.mark.regression
@allure.feature("Todo API")
@allure.story("PUT")
@allure.title("Opdater todo completed status")
@allure.description(
    "Testdesign: Ækvivalenspartitionering<br>"
    "Beskrivelse: Opdaterer completed-feltet på en eksisterende todo<br>"
    "Forventet: HTTP 200 og completed = true"
)
def test_opdater_todo_completed(created_todo, db_session):
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
        '<tr><td style="padding: 8px;">db_todo is not None</td><td style="padding: 8px;">Rækken eksisterer i databasen</td></tr>'
        '<tr><td style="padding: 8px;">db_todo.id == todo_id</td><td style="padding: 8px;">ID matcher det opdaterede todo</td></tr>'
        '<tr><td style="padding: 8px;">db_todo.id > 0</td><td style="padding: 8px;">ID er positivt</td></tr>'
        '<tr><td style="padding: 8px;">db_todo.title == "Test todo"</td><td style="padding: 8px;">Title er uændret i databasen</td></tr>'
        '<tr><td style="padding: 8px;">db_todo.title != ""</td><td style="padding: 8px;">Title er ikke tom</td></tr>'
        '<tr><td style="padding: 8px;">db_todo.completed == True</td><td style="padding: 8px;">Completed er korrekt opdateret til True</td></tr>'
        '<tr><td style="padding: 8px;">isinstance(completed, bool)</td><td style="padding: 8px;">Completed er en boolean</td></tr>'
        "</table>",
        name="Database assertions",
        attachment_type=allure.attachment_type.HTML
    )

    allure.attach(put_diagram(created_todo["title"], True), name="Flow Diagram", attachment_type=allure.attachment_type.HTML)


@pytest.mark.regression
@pytest.mark.negative
@allure.feature("Todo API")
@allure.story("PUT")
@allure.title("Opdater todo der ikke findes")
@allure.description("Testdesign: Negativ test\nBeskrivelse: Forsøger at opdatere en todo med et id der ikke eksisterer\nForventet: HTTP 404")
def test_opdater_todo_der_ikke_findes(db_session):
    """
    Testdesign: Negativ test
    Beskrivelse: Forsøger at opdatere en todo med et id der ikke eksisterer
    Forudsætning: Todo med id 99999 eksisterer ikke i API'et
    Forventet resultat: HTTP 404
    """
    db_todo = db_session.query(TodoDB).filter_by(id=99999).first()
    assert db_todo is None

    response = requests.put(f"{BASE_URL}/todos/99999", json={"title": "Findes ikke"})
    print(f"\nResponse status: {response.status_code}")
    assert response.status_code == 404

    allure.attach(
        '<table border="1" style="border-collapse: collapse; width: 100%;">'
        '<tr style="background-color: #f2f2f2;"><th style="padding: 8px; text-align: left;">Assertion</th><th style="padding: 8px; text-align: left;">Forventet</th></tr>'
        '<tr><td style="padding: 8px;">db_todo is None</td><td style="padding: 8px;">ID 99999 eksisterer ikke i databasen</td></tr>'
        '<tr><td style="padding: 8px;">response.status_code == 404</td><td style="padding: 8px;">HTTP 404</td></tr>'
        "</table>",
        name="Database assertions",
        attachment_type=allure.attachment_type.HTML
    )

    allure.attach(negative_put_diagram(99999), name="Flow Diagram", attachment_type=allure.attachment_type.HTML)


@pytest.mark.regression
@allure.feature("Todo API")
@allure.story("PUT")
@allure.title("Opdater todo med tomt objekt")
@allure.description(
    "Testdesign: Ækvivalenspartitionering<br>"
    "Beskrivelse: Opdaterer en todo med et tomt objekt<br>"
    "Forventet: HTTP 200 og todo er uændret"
)
def test_opdater_todo_med_tomt_objekt(created_todo, db_session):
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
        '<tr><td style="padding: 8px;">db_todo is not None</td><td style="padding: 8px;">Rækken eksisterer i databasen</td></tr>'
        '<tr><td style="padding: 8px;">db_todo.id == todo_id</td><td style="padding: 8px;">ID matcher det opdaterede todo</td></tr>'
        '<tr><td style="padding: 8px;">db_todo.id > 0</td><td style="padding: 8px;">ID er positivt</td></tr>'
        '<tr><td style="padding: 8px;">db_todo.title == created_todo["title"]</td><td style="padding: 8px;">Title er uændret i databasen</td></tr>'
        '<tr><td style="padding: 8px;">db_todo.title != ""</td><td style="padding: 8px;">Title er ikke tom</td></tr>'
        '<tr><td style="padding: 8px;">db_todo.completed == created_todo["completed"]</td><td style="padding: 8px;">Completed er uændret i databasen</td></tr>'
        '<tr><td style="padding: 8px;">isinstance(completed, bool)</td><td style="padding: 8px;">Completed er en boolean</td></tr>'
        "</table>",
        name="Database assertions",
        attachment_type=allure.attachment_type.HTML
    )

    allure.attach(put_diagram(created_todo["title"], created_todo["completed"]), name="Flow Diagram", attachment_type=allure.attachment_type.HTML)


@pytest.mark.regression
@allure.feature("Todo API")
@allure.story("PUT")
@allure.title("Valider felter i PUT response")
@allure.description(
    "Testdesign: Ækvivalenspartitionering<br>"
    "Beskrivelse: Validerer at response indeholder alle forventede felter efter opdatering<br>"
    "Forventet: HTTP 200 og response indeholder id, title, completed"
)
def test_valider_felter_i_response(created_todo, db_session):
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
        '<tr><td style="padding: 8px;">db_todo is not None</td><td style="padding: 8px;">Rækken eksisterer i databasen</td></tr>'
        '<tr><td style="padding: 8px;">db_todo.id == todo_id</td><td style="padding: 8px;">ID matcher det opdaterede todo</td></tr>'
        '<tr><td style="padding: 8px;">db_todo.id > 0</td><td style="padding: 8px;">ID er positivt</td></tr>'
        '<tr><td style="padding: 8px;">db_todo.title == "Opdateret"</td><td style="padding: 8px;">Title er korrekt opdateret i databasen</td></tr>'
        '<tr><td style="padding: 8px;">db_todo.title != ""</td><td style="padding: 8px;">Title er ikke tom</td></tr>'
        '<tr><td style="padding: 8px;">db_todo.completed == False</td><td style="padding: 8px;">Completed er uændret (False)</td></tr>'
        '<tr><td style="padding: 8px;">isinstance(completed, bool)</td><td style="padding: 8px;">Completed er en boolean</td></tr>'
        "</table>",
        name="Database assertions",
        attachment_type=allure.attachment_type.HTML
    )

    allure.attach(put_diagram("Opdateret", False), name="Flow Diagram", attachment_type=allure.attachment_type.HTML)
