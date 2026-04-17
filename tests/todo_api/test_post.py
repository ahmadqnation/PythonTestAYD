import pytest
import allure
import requests
from tests.todo_api.conftest import BASE_URL
from api.models_db import TodoDB
from tests.todo_api.diagrams import post_diagram, negative_post_diagram
from tests.todo_api.testdesign_tables import post_equivalence_table, post_boundary_table

_REQS = {
    "REQ-001": "Title skal have minimum 1 tegn",
    "REQ-002": "Title skal have maximum 500 tegn",
    "REQ-003": "Completed skal være boolean (true/false)",
    "REQ-004": "ID genereres automatisk og er unikt og positivt",
    "REQ-006": "POST /todos returnerer HTTP 201 og opretter todo",
    "REQ-010": "Tom title returnerer HTTP 422",
    "REQ-011": "Title over 500 tegn returnerer HTTP 422",
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
@allure.story("001B_POST")
@allure.title("Opret todo med alle gyldige felter og valider response")
@allure.description(
    "Beskrivelse: Opretter en todo med alle gyldige felter og verificerer at response indeholder id, title og completed<br>"
    "Forventet: HTTP 201 og response indeholder alle forventede felter"
)
def test_opret_todo(new_todo, db_session):
    """
    Testdesign: Ækvivalenspartitionering
    Beskrivelse: Opretter en todo med alle gyldige felter og verificerer response felter
    Forudsætning: API'et er tilgængeligt og accepterer POST requests
    Forventet resultat: HTTP 201 og response indeholder id, title, completed
    """
    response = requests.post(f"{BASE_URL}/todos", json=new_todo)
    todo = response.json()
    print(f"\nResponse: {todo}")
    assert response.status_code == 201
    assert response.elapsed.total_seconds() < 2
    assert "application/json" in response.headers["Content-Type"]
    assert todo["title"] == new_todo["title"]
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
        '<tr><td style="padding: 8px;">response.status_code == 201</td><td style="padding: 8px;">HTTP 201</td></tr>'
        '<tr><td style="padding: 8px;">response.elapsed.total_seconds() &lt; 2</td><td style="padding: 8px;">Responstid under 2 sekunder (REQ-012)</td></tr>'
        '<tr><td style="padding: 8px;">"application/json" in Content-Type</td><td style="padding: 8px;">Response er JSON format (REQ-014)</td></tr>'
        '<tr><td style="padding: 8px;">todo["title"] == new_todo["title"]</td><td style="padding: 8px;">Title matcher det vi sendte</td></tr>'
        '<tr><td style="padding: 8px;">all(felt in todo for felt in [...])</td><td style="padding: 8px;">Response indeholder id, title, completed</td></tr>'
        '<tr><td style="padding: 8px;">db_todo is not None</td><td style="padding: 8px;">Rækken eksisterer i databasen (REQ-015)</td></tr>'
        '<tr><td style="padding: 8px;">db_todo.id == todo["id"]</td><td style="padding: 8px;">ID matcher API response</td></tr>'
        '<tr><td style="padding: 8px;">db_todo.id > 0</td><td style="padding: 8px;">ID er positivt (REQ-004)</td></tr>'
        '<tr><td style="padding: 8px;">db_todo.title == new_todo["title"]</td><td style="padding: 8px;">Title matcher det vi sendte</td></tr>'
        '<tr><td style="padding: 8px;">db_todo.title != ""</td><td style="padding: 8px;">Title er ikke tom</td></tr>'
        '<tr><td style="padding: 8px;">db_todo.completed == new_todo["completed"]</td><td style="padding: 8px;">Completed matcher det vi sendte (REQ-003)</td></tr>'
        '<tr><td style="padding: 8px;">isinstance(completed, bool)</td><td style="padding: 8px;">Completed er en boolean (REQ-003)</td></tr>'
        "</table>",
        name="Database assertions",
        attachment_type=allure.attachment_type.HTML
    )

    allure.attach(post_equivalence_table("K1"), name="Testdesign", attachment_type=allure.attachment_type.HTML)
    allure.attach(post_diagram(new_todo["title"], new_todo["completed"]), name="Flow Diagram", attachment_type=allure.attachment_type.HTML)
    _link_reqs("REQ-003", "REQ-004", "REQ-006", "REQ-012", "REQ-013", "REQ-014", "REQ-015")

    requests.delete(f"{BASE_URL}/todos/{todo['id']}")


@pytest.mark.regression
@pytest.mark.negative
@allure.feature("001_Tests")
@allure.story("001B_POST")
@allure.title("Opret todo uden titel")
@allure.description("Beskrivelse: Forsøger at oprette en todo uden det påkrævede titel-felt\nForventet: HTTP 422")
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
    assert response.elapsed.total_seconds() < 2

    db_session.expire_all()
    count_after = db_session.query(TodoDB).count()
    assert count_after == count_before

    allure.attach(
        '<table border="1" style="border-collapse: collapse; width: 100%;">'
        '<tr style="background-color: #f2f2f2;"><th style="padding: 8px; text-align: left;">Assertion</th><th style="padding: 8px; text-align: left;">Forventet</th></tr>'
        '<tr><td style="padding: 8px;">response.status_code == 422</td><td style="padding: 8px;">HTTP 422 (FastAPI validerer manglende felt)</td></tr>'
        '<tr><td style="padding: 8px;">response.elapsed.total_seconds() &lt; 2</td><td style="padding: 8px;">Responstid under 2 sekunder (REQ-012)</td></tr>'
        '<tr><td style="padding: 8px;">count_before (baseline)</td><td style="padding: 8px;">Registrerer antal rækker inden kaldet</td></tr>'
        '<tr><td style="padding: 8px;">count_after == count_before</td><td style="padding: 8px;">Ingen rækker oprettet i databasen (REQ-015)</td></tr>'
        "</table>",
        name="Database assertions",
        attachment_type=allure.attachment_type.HTML
    )

    allure.attach(post_equivalence_table("K4"), name="Testdesign", attachment_type=allure.attachment_type.HTML)
    allure.attach(negative_post_diagram("title"), name="Flow Diagram", attachment_type=allure.attachment_type.HTML)
    _link_reqs("REQ-006", "REQ-012", "REQ-013", "REQ-015")


@pytest.mark.regression
@allure.feature("001_Tests")
@allure.story("001B_POST")
@allure.title("Opret todo med completed false som default")
@allure.description(
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
    assert response.elapsed.total_seconds() < 2
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
        '<tr><td style="padding: 8px;">response.status_code == 201</td><td style="padding: 8px;">HTTP 201</td></tr>'
        '<tr><td style="padding: 8px;">response.elapsed.total_seconds() &lt; 2</td><td style="padding: 8px;">Responstid under 2 sekunder (REQ-012)</td></tr>'
        '<tr><td style="padding: 8px;">db_todo is not None</td><td style="padding: 8px;">Rækken eksisterer i databasen (REQ-015)</td></tr>'
        '<tr><td style="padding: 8px;">db_todo.id == todo["id"]</td><td style="padding: 8px;">ID matcher API response</td></tr>'
        '<tr><td style="padding: 8px;">db_todo.id > 0</td><td style="padding: 8px;">ID er positivt (REQ-004)</td></tr>'
        '<tr><td style="padding: 8px;">db_todo.title == "Default completed test"</td><td style="padding: 8px;">Title matcher det vi sendte</td></tr>'
        '<tr><td style="padding: 8px;">db_todo.title != ""</td><td style="padding: 8px;">Title er ikke tom</td></tr>'
        '<tr><td style="padding: 8px;">db_todo.completed == False</td><td style="padding: 8px;">Completed er False (API default) (REQ-003)</td></tr>'
        '<tr><td style="padding: 8px;">isinstance(completed, bool)</td><td style="padding: 8px;">Completed er en boolean (REQ-003)</td></tr>'
        "</table>",
        name="Database assertions",
        attachment_type=allure.attachment_type.HTML
    )

    allure.attach(post_equivalence_table("K2"), name="Testdesign", attachment_type=allure.attachment_type.HTML)
    allure.attach(post_diagram(todo_input["title"], todo["completed"]), name="Flow Diagram", attachment_type=allure.attachment_type.HTML)
    _link_reqs("REQ-003", "REQ-004", "REQ-006", "REQ-012", "REQ-013", "REQ-015")

    requests.delete(f"{BASE_URL}/todos/{todo['id']}")


@pytest.mark.regression
@allure.feature("001_Tests")
@allure.story("001B_POST")
@allure.title("Opret todo med completed true")
@allure.description(
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
    assert response.elapsed.total_seconds() < 2
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
        '<tr><td style="padding: 8px;">response.status_code == 201</td><td style="padding: 8px;">HTTP 201</td></tr>'
        '<tr><td style="padding: 8px;">response.elapsed.total_seconds() &lt; 2</td><td style="padding: 8px;">Responstid under 2 sekunder (REQ-012)</td></tr>'
        '<tr><td style="padding: 8px;">db_todo is not None</td><td style="padding: 8px;">Rækken eksisterer i databasen (REQ-015)</td></tr>'
        '<tr><td style="padding: 8px;">db_todo.id == todo["id"]</td><td style="padding: 8px;">ID matcher API response</td></tr>'
        '<tr><td style="padding: 8px;">db_todo.id > 0</td><td style="padding: 8px;">ID er positivt (REQ-004)</td></tr>'
        '<tr><td style="padding: 8px;">db_todo.title == "Færdig todo"</td><td style="padding: 8px;">Title matcher det vi sendte</td></tr>'
        '<tr><td style="padding: 8px;">db_todo.title != ""</td><td style="padding: 8px;">Title er ikke tom</td></tr>'
        '<tr><td style="padding: 8px;">db_todo.completed == True</td><td style="padding: 8px;">Completed matcher det vi sendte (True) (REQ-003)</td></tr>'
        '<tr><td style="padding: 8px;">isinstance(completed, bool)</td><td style="padding: 8px;">Completed er en boolean (REQ-003)</td></tr>'
        "</table>",
        name="Database assertions",
        attachment_type=allure.attachment_type.HTML
    )

    allure.attach(post_equivalence_table("K3"), name="Testdesign", attachment_type=allure.attachment_type.HTML)
    allure.attach(post_diagram(todo_input["title"], todo_input["completed"]), name="Flow Diagram", attachment_type=allure.attachment_type.HTML)
    _link_reqs("REQ-003", "REQ-004", "REQ-006", "REQ-012", "REQ-013", "REQ-015")

    requests.delete(f"{BASE_URL}/todos/{todo['id']}")


@pytest.mark.regression
@allure.feature("001_Tests")
@allure.story("001B_POST")
@allure.title("Opret todo med lang titel (500 tegn)")
@allure.description(
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
    assert response.elapsed.total_seconds() < 2
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
        '<tr><td style="padding: 8px;">response.status_code == 201</td><td style="padding: 8px;">HTTP 201</td></tr>'
        '<tr><td style="padding: 8px;">response.elapsed.total_seconds() &lt; 2</td><td style="padding: 8px;">Responstid under 2 sekunder (REQ-012)</td></tr>'
        '<tr><td style="padding: 8px;">db_todo is not None</td><td style="padding: 8px;">Rækken eksisterer i databasen (REQ-015)</td></tr>'
        '<tr><td style="padding: 8px;">db_todo.id == todo["id"]</td><td style="padding: 8px;">ID matcher API response</td></tr>'
        '<tr><td style="padding: 8px;">db_todo.id > 0</td><td style="padding: 8px;">ID er positivt (REQ-004)</td></tr>'
        '<tr><td style="padding: 8px;">db_todo.title == "a" * 500</td><td style="padding: 8px;">Title er 500 tegn lang (REQ-002)</td></tr>'
        '<tr><td style="padding: 8px;">db_todo.title != ""</td><td style="padding: 8px;">Title er ikke tom</td></tr>'
        '<tr><td style="padding: 8px;">db_todo.completed == False</td><td style="padding: 8px;">Completed er False (API default) (REQ-003)</td></tr>'
        '<tr><td style="padding: 8px;">isinstance(completed, bool)</td><td style="padding: 8px;">Completed er en boolean (REQ-003)</td></tr>'
        "</table>",
        name="Database assertions",
        attachment_type=allure.attachment_type.HTML
    )

    allure.attach(post_boundary_table("BV3"), name="Testdesign", attachment_type=allure.attachment_type.HTML)
    allure.attach(post_diagram(lang_titel, todo["completed"]), name="Flow Diagram", attachment_type=allure.attachment_type.HTML)
    _link_reqs("REQ-002", "REQ-004", "REQ-006", "REQ-012", "REQ-013", "REQ-015")

    requests.delete(f"{BASE_URL}/todos/{todo['id']}")


@pytest.mark.regression
@pytest.mark.negative
@allure.feature("001_Tests")
@allure.story("001B_POST")
@allure.title("Opret todo med tom titel (0 tegn)")
@allure.description(
    "Beskrivelse: Forsøger at oprette en todo med en tom title (0 tegn, under nedre grænse)<br>"
    "Forventet: HTTP 422"
)
def test_opret_todo_med_tom_titel(db_session):
    """
    Testdesign: Grænseværdianalyse
    Beskrivelse: Forsøger at oprette en todo med en tom title (0 tegn, under nedre grænse)
    Forudsætning: API'et validerer at title ikke er tom
    Forventet resultat: HTTP 422
    """
    count_before = db_session.query(TodoDB).count()

    response = requests.post(f"{BASE_URL}/todos", json={"title": ""})
    print(f"\nResponse: {response.status_code}")
    assert response.status_code == 422
    assert response.elapsed.total_seconds() < 2

    db_session.expire_all()
    count_after = db_session.query(TodoDB).count()
    assert count_after == count_before

    allure.attach(
        '<table border="1" style="border-collapse: collapse; width: 100%;">'
        '<tr style="background-color: #f2f2f2;"><th style="padding: 8px; text-align: left;">Assertion</th><th style="padding: 8px; text-align: left;">Forventet</th></tr>'
        '<tr><td style="padding: 8px;">response.status_code == 422</td><td style="padding: 8px;">HTTP 422 (tom title afvises) (REQ-010)</td></tr>'
        '<tr><td style="padding: 8px;">response.elapsed.total_seconds() &lt; 2</td><td style="padding: 8px;">Responstid under 2 sekunder (REQ-012)</td></tr>'
        '<tr><td style="padding: 8px;">count_before (baseline)</td><td style="padding: 8px;">Registrerer antal rækker inden kaldet</td></tr>'
        '<tr><td style="padding: 8px;">count_after == count_before</td><td style="padding: 8px;">Ingen rækker oprettet i databasen (REQ-015)</td></tr>'
        "</table>",
        name="Database assertions",
        attachment_type=allure.attachment_type.HTML
    )

    allure.attach(post_boundary_table("BV1"), name="Testdesign", attachment_type=allure.attachment_type.HTML)
    allure.attach(negative_post_diagram('title=""'), name="Flow Diagram", attachment_type=allure.attachment_type.HTML)
    _link_reqs("REQ-001", "REQ-010", "REQ-012", "REQ-013", "REQ-015")


@pytest.mark.regression
@allure.feature("001_Tests")
@allure.story("001B_POST")
@allure.title("Opret todo med enkelt tegn i titel (1 tegn)")
@allure.description(
    "Beskrivelse: Opretter en todo med en title på 1 tegn (nedre grænse)<br>"
    "Forventet: HTTP 201 og title er 1 tegn lang"
)
def test_opret_todo_med_enkelt_tegn(db_session):
    """
    Testdesign: Grænseværdianalyse
    Beskrivelse: Opretter en todo med en title på 1 tegn (nedre grænse)
    Forudsætning: API'et accepterer title med minimum 1 tegn
    Forventet resultat: HTTP 201 og title er 1 tegn lang
    """
    response = requests.post(f"{BASE_URL}/todos", json={"title": "a"})
    todo = response.json()
    assert response.status_code == 201
    assert response.elapsed.total_seconds() < 2
    assert len(todo["title"]) == 1

    db_todo = db_session.query(TodoDB).filter_by(id=todo["id"]).first()
    assert db_todo is not None
    assert db_todo.id == todo["id"]
    assert db_todo.id > 0
    assert db_todo.title == "a"
    assert db_todo.title != ""
    assert db_todo.completed == todo["completed"]
    assert isinstance(db_todo.completed, bool)

    allure.attach(
        '<table border="1" style="border-collapse: collapse; width: 100%;">'
        '<tr style="background-color: #f2f2f2;"><th style="padding: 8px; text-align: left;">Assertion</th><th style="padding: 8px; text-align: left;">Forventet</th></tr>'
        '<tr><td style="padding: 8px;">response.status_code == 201</td><td style="padding: 8px;">HTTP 201</td></tr>'
        '<tr><td style="padding: 8px;">response.elapsed.total_seconds() &lt; 2</td><td style="padding: 8px;">Responstid under 2 sekunder (REQ-012)</td></tr>'
        '<tr><td style="padding: 8px;">len(todo["title"]) == 1</td><td style="padding: 8px;">Title er præcis 1 tegn lang (REQ-001)</td></tr>'
        '<tr><td style="padding: 8px;">db_todo is not None</td><td style="padding: 8px;">Rækken eksisterer i databasen (REQ-015)</td></tr>'
        '<tr><td style="padding: 8px;">db_todo.id == todo["id"]</td><td style="padding: 8px;">ID matcher API response</td></tr>'
        '<tr><td style="padding: 8px;">db_todo.id > 0</td><td style="padding: 8px;">ID er positivt (REQ-004)</td></tr>'
        '<tr><td style="padding: 8px;">db_todo.title == "a"</td><td style="padding: 8px;">Title er korrekt gemt i databasen</td></tr>'
        '<tr><td style="padding: 8px;">db_todo.title != ""</td><td style="padding: 8px;">Title er ikke tom</td></tr>'
        '<tr><td style="padding: 8px;">db_todo.completed == False</td><td style="padding: 8px;">Completed er False (API default) (REQ-003)</td></tr>'
        '<tr><td style="padding: 8px;">isinstance(completed, bool)</td><td style="padding: 8px;">Completed er en boolean (REQ-003)</td></tr>'
        "</table>",
        name="Database assertions",
        attachment_type=allure.attachment_type.HTML
    )

    allure.attach(post_boundary_table("BV2"), name="Testdesign", attachment_type=allure.attachment_type.HTML)
    allure.attach(post_diagram("a", todo["completed"]), name="Flow Diagram", attachment_type=allure.attachment_type.HTML)
    _link_reqs("REQ-001", "REQ-004", "REQ-006", "REQ-012", "REQ-013", "REQ-015")

    requests.delete(f"{BASE_URL}/todos/{todo['id']}")


@pytest.mark.regression
@pytest.mark.negative
@allure.feature("001_Tests")
@allure.story("001B_POST")
@allure.title("Opret todo over max længde (501 tegn)")
@allure.description(
    "Beskrivelse: Forsøger at oprette en todo med en title på 501 tegn (over øvre grænse)<br>"
    "Forventet: HTTP 422"
)
def test_opret_todo_over_max_laengde(db_session):
    """
    Testdesign: Grænseværdianalyse
    Beskrivelse: Forsøger at oprette en todo med en title på 501 tegn (over øvre grænse)
    Forudsætning: API'et afviser titles over 500 tegn
    Forventet resultat: HTTP 422
    """
    count_before = db_session.query(TodoDB).count()

    response = requests.post(f"{BASE_URL}/todos", json={"title": "a" * 501})
    print(f"\nResponse: {response.status_code}")
    assert response.status_code == 422
    assert response.elapsed.total_seconds() < 2

    db_session.expire_all()
    count_after = db_session.query(TodoDB).count()
    assert count_after == count_before

    allure.attach(
        '<table border="1" style="border-collapse: collapse; width: 100%;">'
        '<tr style="background-color: #f2f2f2;"><th style="padding: 8px; text-align: left;">Assertion</th><th style="padding: 8px; text-align: left;">Forventet</th></tr>'
        '<tr><td style="padding: 8px;">response.status_code == 422</td><td style="padding: 8px;">HTTP 422 (title over max længde afvises) (REQ-011)</td></tr>'
        '<tr><td style="padding: 8px;">response.elapsed.total_seconds() &lt; 2</td><td style="padding: 8px;">Responstid under 2 sekunder (REQ-012)</td></tr>'
        '<tr><td style="padding: 8px;">count_before (baseline)</td><td style="padding: 8px;">Registrerer antal rækker inden kaldet</td></tr>'
        '<tr><td style="padding: 8px;">count_after == count_before</td><td style="padding: 8px;">Ingen rækker oprettet i databasen (REQ-015)</td></tr>'
        "</table>",
        name="Database assertions",
        attachment_type=allure.attachment_type.HTML
    )

    allure.attach(post_boundary_table("BV4"), name="Testdesign", attachment_type=allure.attachment_type.HTML)
    allure.attach(negative_post_diagram("501 tegn"), name="Flow Diagram", attachment_type=allure.attachment_type.HTML)
    _link_reqs("REQ-002", "REQ-011", "REQ-012", "REQ-013", "REQ-015")
