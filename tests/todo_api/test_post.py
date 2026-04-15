import pytest
import allure
import requests
from tests.todo_api.conftest import BASE_URL
from api.models_db import TodoDB
from tests.todo_api.diagrams import post_diagram, negative_post_diagram


@pytest.mark.smoke
@pytest.mark.regression
@allure.feature("Todo API")
@allure.story("POST")
@allure.title("Opret todo med alle gyldige felter")
@allure.description(
    "Testdesign: Ækvivalenspartitionering<br>"
    "Beskrivelse: Opretter en todo med alle gyldige felter<br>"
    "Forventet: HTTP 201 og response indeholder den sendte titel"
)
def test_opret_todo(new_todo, db_session):
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

    db_todo = db_session.query(TodoDB).filter_by(id=todo["id"]).first()
    assert db_todo is not None
    assert db_todo.id == todo["id"]
    assert db_todo.id > 0
    assert db_todo.title == new_todo["title"]
    assert db_todo.title != ""
    assert db_todo.completed == new_todo["completed"]
    assert isinstance(db_todo.completed, bool)

    allure.attach(
        '<table border="1" style="border-collapse: collapse; width: 100%;">'
        '<tr style="background-color: #f2f2f2;"><th style="padding: 8px; text-align: left;">Assertion</th><th style="padding: 8px; text-align: left;">Forventet</th></tr>'
        '<tr><td style="padding: 8px;">db_todo is not None</td><td style="padding: 8px;">Rækken eksisterer i databasen</td></tr>'
        '<tr><td style="padding: 8px;">db_todo.id == todo["id"]</td><td style="padding: 8px;">ID matcher API response</td></tr>'
        '<tr><td style="padding: 8px;">db_todo.id > 0</td><td style="padding: 8px;">ID er positivt</td></tr>'
        '<tr><td style="padding: 8px;">db_todo.title == "Test todo"</td><td style="padding: 8px;">Title matcher det vi sendte</td></tr>'
        '<tr><td style="padding: 8px;">db_todo.title != ""</td><td style="padding: 8px;">Title er ikke tom</td></tr>'
        '<tr><td style="padding: 8px;">db_todo.completed == False</td><td style="padding: 8px;">Completed matcher det vi sendte (False)</td></tr>'
        '<tr><td style="padding: 8px;">isinstance(completed, bool)</td><td style="padding: 8px;">Completed er en boolean</td></tr>'
        "</table>",
        name="Database assertions",
        attachment_type=allure.attachment_type.HTML
    )

    allure.attach(post_diagram(new_todo["title"], new_todo["completed"]), name="Flow Diagram", attachment_type=allure.attachment_type.HTML)

    requests.delete(f"{BASE_URL}/todos/{todo['id']}")


@pytest.mark.regression
@pytest.mark.negative
@allure.feature("Todo API")
@allure.story("POST")
@allure.title("Opret todo uden titel")
@allure.description("Testdesign: Negativ test\nBeskrivelse: Forsøger at oprette en todo uden det påkrævede titel-felt\nForventet: HTTP 422")
def test_opret_todo_uden_titel(db_session):
    """
    Testdesign: Negativ test
    Beskrivelse: Forsøger at oprette en todo uden det påkrævede titel-felt
    Forudsætning: API'et kræver title-feltet
    Forventet resultat: HTTP 422 (FastAPI validering)
    """
    count_before = db_session.query(TodoDB).count()

    response = requests.post(f"{BASE_URL}/todos", json={"completed": False})
    print(f"\nResponse: {response.status_code}")
    assert response.status_code == 422

    db_session.expire_all()
    count_after = db_session.query(TodoDB).count()
    assert count_after == count_before

    allure.attach(
        '<table border="1" style="border-collapse: collapse; width: 100%;">'
        '<tr style="background-color: #f2f2f2;"><th style="padding: 8px; text-align: left;">Assertion</th><th style="padding: 8px; text-align: left;">Forventet</th></tr>'
        '<tr><td style="padding: 8px;">count_before (baseline)</td><td style="padding: 8px;">Registrerer antal rækker inden kaldet</td></tr>'
        '<tr><td style="padding: 8px;">response.status_code == 422</td><td style="padding: 8px;">HTTP 422 (FastAPI validerer manglende felt)</td></tr>'
        '<tr><td style="padding: 8px;">count_after == count_before</td><td style="padding: 8px;">Ingen rækker oprettet i databasen</td></tr>'
        "</table>",
        name="Database assertions",
        attachment_type=allure.attachment_type.HTML
    )

    allure.attach(negative_post_diagram("title"), name="Flow Diagram", attachment_type=allure.attachment_type.HTML)


@pytest.mark.regression
@allure.feature("Todo API")
@allure.story("POST")
@allure.title("Opret todo med completed false som default")
@allure.description(
    "Testdesign: Ækvivalenspartitionering<br>"
    "Beskrivelse: Opretter en todo uden completed-feltet og verificerer default-værdien<br>"
    "Forventet: HTTP 201 og completed = false"
)
def test_opret_todo_completed_false_som_default(db_session):
    """
    Testdesign: Ækvivalenspartitionering
    Beskrivelse: Opretter en todo uden completed-feltet og verificerer default-værdien
    Forudsætning: API'et sætter completed til false som standard
    Forventet resultat: HTTP 201 og completed = false
    """
    todo_input = {"title": "Default completed test"}
    response = requests.post(f"{BASE_URL}/todos", json=todo_input)
    todo = response.json()
    assert response.status_code == 201
    assert todo["completed"] is False

    db_todo = db_session.query(TodoDB).filter_by(id=todo["id"]).first()
    assert db_todo is not None
    assert db_todo.id == todo["id"]
    assert db_todo.id > 0
    assert db_todo.title == todo_input["title"]
    assert db_todo.title != ""
    assert db_todo.completed == todo["completed"]
    assert isinstance(db_todo.completed, bool)

    allure.attach(
        '<table border="1" style="border-collapse: collapse; width: 100%;">'
        '<tr style="background-color: #f2f2f2;"><th style="padding: 8px; text-align: left;">Assertion</th><th style="padding: 8px; text-align: left;">Forventet</th></tr>'
        '<tr><td style="padding: 8px;">db_todo is not None</td><td style="padding: 8px;">Rækken eksisterer i databasen</td></tr>'
        '<tr><td style="padding: 8px;">db_todo.id == todo["id"]</td><td style="padding: 8px;">ID matcher API response</td></tr>'
        '<tr><td style="padding: 8px;">db_todo.id > 0</td><td style="padding: 8px;">ID er positivt</td></tr>'
        '<tr><td style="padding: 8px;">db_todo.title == "Default completed test"</td><td style="padding: 8px;">Title matcher det vi sendte</td></tr>'
        '<tr><td style="padding: 8px;">db_todo.title != ""</td><td style="padding: 8px;">Title er ikke tom</td></tr>'
        '<tr><td style="padding: 8px;">db_todo.completed == False</td><td style="padding: 8px;">Completed er False (API default)</td></tr>'
        '<tr><td style="padding: 8px;">isinstance(completed, bool)</td><td style="padding: 8px;">Completed er en boolean</td></tr>'
        "</table>",
        name="Database assertions",
        attachment_type=allure.attachment_type.HTML
    )

    allure.attach(post_diagram(todo_input["title"], todo["completed"]), name="Flow Diagram", attachment_type=allure.attachment_type.HTML)

    requests.delete(f"{BASE_URL}/todos/{todo['id']}")


@pytest.mark.regression
@allure.feature("Todo API")
@allure.story("POST")
@allure.title("Opret todo med completed true")
@allure.description(
    "Testdesign: Ækvivalenspartitionering<br>"
    "Beskrivelse: Opretter en todo med completed sat til true<br>"
    "Forventet: HTTP 201 og completed = true"
)
def test_opret_todo_med_completed_true(db_session):
    """
    Testdesign: Ækvivalenspartitionering
    Beskrivelse: Opretter en todo med completed sat til true
    Forudsætning: API'et accepterer completed = true
    Forventet resultat: HTTP 201 og completed = true
    """
    todo_input = {"title": "Færdig todo", "completed": True}
    response = requests.post(f"{BASE_URL}/todos", json=todo_input)
    todo = response.json()
    assert response.status_code == 201
    assert todo["completed"] is True

    db_todo = db_session.query(TodoDB).filter_by(id=todo["id"]).first()
    assert db_todo is not None
    assert db_todo.id == todo["id"]
    assert db_todo.id > 0
    assert db_todo.title == todo_input["title"]
    assert db_todo.title != ""
    assert db_todo.completed == todo_input["completed"]
    assert isinstance(db_todo.completed, bool)

    allure.attach(
        '<table border="1" style="border-collapse: collapse; width: 100%;">'
        '<tr style="background-color: #f2f2f2;"><th style="padding: 8px; text-align: left;">Assertion</th><th style="padding: 8px; text-align: left;">Forventet</th></tr>'
        '<tr><td style="padding: 8px;">db_todo is not None</td><td style="padding: 8px;">Rækken eksisterer i databasen</td></tr>'
        '<tr><td style="padding: 8px;">db_todo.id == todo["id"]</td><td style="padding: 8px;">ID matcher API response</td></tr>'
        '<tr><td style="padding: 8px;">db_todo.id > 0</td><td style="padding: 8px;">ID er positivt</td></tr>'
        '<tr><td style="padding: 8px;">db_todo.title == "Færdig todo"</td><td style="padding: 8px;">Title matcher det vi sendte</td></tr>'
        '<tr><td style="padding: 8px;">db_todo.title != ""</td><td style="padding: 8px;">Title er ikke tom</td></tr>'
        '<tr><td style="padding: 8px;">db_todo.completed == True</td><td style="padding: 8px;">Completed matcher det vi sendte (True)</td></tr>'
        '<tr><td style="padding: 8px;">isinstance(completed, bool)</td><td style="padding: 8px;">Completed er en boolean</td></tr>'
        "</table>",
        name="Database assertions",
        attachment_type=allure.attachment_type.HTML
    )

    allure.attach(post_diagram(todo_input["title"], todo_input["completed"]), name="Flow Diagram", attachment_type=allure.attachment_type.HTML)

    requests.delete(f"{BASE_URL}/todos/{todo['id']}")


@pytest.mark.regression
@allure.feature("Todo API")
@allure.story("POST")
@allure.title("Valider felter i POST response")
@allure.description(
    "Testdesign: Ækvivalenspartitionering<br>"
    "Beskrivelse: Validerer at response indeholder alle forventede felter efter oprettelse<br>"
    "Forventet: HTTP 201 og response indeholder id, title, completed"
)
def test_valider_felter_i_response(new_todo, db_session):
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

    db_todo = db_session.query(TodoDB).filter_by(id=todo["id"]).first()
    assert db_todo is not None
    assert db_todo.id == todo["id"]
    assert db_todo.id > 0
    assert db_todo.title == new_todo["title"]
    assert db_todo.title != ""
    assert db_todo.completed == new_todo["completed"]
    assert isinstance(db_todo.completed, bool)

    allure.attach(
        '<table border="1" style="border-collapse: collapse; width: 100%;">'
        '<tr style="background-color: #f2f2f2;"><th style="padding: 8px; text-align: left;">Assertion</th><th style="padding: 8px; text-align: left;">Forventet</th></tr>'
        '<tr><td style="padding: 8px;">db_todo is not None</td><td style="padding: 8px;">Rækken eksisterer i databasen</td></tr>'
        '<tr><td style="padding: 8px;">db_todo.id == todo["id"]</td><td style="padding: 8px;">ID matcher API response</td></tr>'
        '<tr><td style="padding: 8px;">db_todo.id > 0</td><td style="padding: 8px;">ID er positivt</td></tr>'
        '<tr><td style="padding: 8px;">db_todo.title == "Test todo"</td><td style="padding: 8px;">Title matcher det vi sendte</td></tr>'
        '<tr><td style="padding: 8px;">db_todo.title != ""</td><td style="padding: 8px;">Title er ikke tom</td></tr>'
        '<tr><td style="padding: 8px;">db_todo.completed == False</td><td style="padding: 8px;">Completed matcher det vi sendte (False)</td></tr>'
        '<tr><td style="padding: 8px;">isinstance(completed, bool)</td><td style="padding: 8px;">Completed er en boolean</td></tr>'
        "</table>",
        name="Database assertions",
        attachment_type=allure.attachment_type.HTML
    )

    allure.attach(post_diagram(new_todo["title"], new_todo["completed"]), name="Flow Diagram", attachment_type=allure.attachment_type.HTML)

    requests.delete(f"{BASE_URL}/todos/{todo['id']}")


@pytest.mark.regression
@allure.feature("Todo API")
@allure.story("POST")
@allure.title("Opret todo med lang titel (500 tegn)")
@allure.description(
    "Testdesign: Grænseværdianalyse<br>"
    "Beskrivelse: Opretter en todo med en titel på 500 tegn (øvre grænse)<br>"
    "Forventet: HTTP 201 og titel i response er 500 tegn lang"
)
def test_opret_todo_med_lang_titel(db_session):
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

    db_todo = db_session.query(TodoDB).filter_by(id=todo["id"]).first()
    assert db_todo is not None
    assert db_todo.id == todo["id"]
    assert db_todo.id > 0
    assert db_todo.title == lang_titel
    assert db_todo.title != ""
    assert db_todo.completed == todo["completed"]
    assert isinstance(db_todo.completed, bool)

    allure.attach(
        '<table border="1" style="border-collapse: collapse; width: 100%;">'
        '<tr style="background-color: #f2f2f2;"><th style="padding: 8px; text-align: left;">Assertion</th><th style="padding: 8px; text-align: left;">Forventet</th></tr>'
        '<tr><td style="padding: 8px;">db_todo is not None</td><td style="padding: 8px;">Rækken eksisterer i databasen</td></tr>'
        '<tr><td style="padding: 8px;">db_todo.id == todo["id"]</td><td style="padding: 8px;">ID matcher API response</td></tr>'
        '<tr><td style="padding: 8px;">db_todo.id > 0</td><td style="padding: 8px;">ID er positivt</td></tr>'
        '<tr><td style="padding: 8px;">db_todo.title == "a" * 500</td><td style="padding: 8px;">Title er 500 tegn lang</td></tr>'
        '<tr><td style="padding: 8px;">db_todo.title != ""</td><td style="padding: 8px;">Title er ikke tom</td></tr>'
        '<tr><td style="padding: 8px;">db_todo.completed == False</td><td style="padding: 8px;">Completed er False (API default)</td></tr>'
        '<tr><td style="padding: 8px;">isinstance(completed, bool)</td><td style="padding: 8px;">Completed er en boolean</td></tr>'
        "</table>",
        name="Database assertions",
        attachment_type=allure.attachment_type.HTML
    )

    allure.attach(post_diagram(lang_titel, todo["completed"]), name="Flow Diagram", attachment_type=allure.attachment_type.HTML)

    requests.delete(f"{BASE_URL}/todos/{todo['id']}")
