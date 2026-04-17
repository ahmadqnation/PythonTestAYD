import pytest
import allure
import requests
from tests.todo_api.conftest import BASE_URL
from api.models_db import TodoDB
from tests.todo_api.diagrams import delete_diagram, negative_delete_diagram
from tests.todo_api.testdesign_tables import delete_equivalence_table

_REQS = {
    "REQ-004": "ID genereres automatisk og er unikt og positivt",
    "REQ-008": "DELETE /todos/{id} returnerer HTTP 200 og sletter todo",
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
@allure.story("001D_DELETE")
@allure.title("Slet eksisterende todo")
@allure.description(
    "Beskrivelse: Sletter en eksisterende todo med gyldigt id<br>"
    "Forventet: HTTP 200"
)
def test_slet_todo(new_todo, db_session):
    """
    Testdesign: Ækvivalenspartitionering
    Beskrivelse: Sletter en eksisterende todo med gyldigt id
    Forudsætning: Todo eksisterer i API'et
    Forventet resultat: HTTP 200
    """
    created = requests.post(f"{BASE_URL}/todos", json=new_todo).json()
    deleted_id = created["id"]

    db_todo_before = db_session.query(TodoDB).filter_by(id=deleted_id).first()
    assert db_todo_before is not None

    response = requests.delete(f"{BASE_URL}/todos/{deleted_id}")
    print(f"\nResponse status: {response.status_code}")
    assert response.status_code == 200
    assert response.elapsed.total_seconds() < 2
    assert "application/json" in response.headers["Content-Type"]

    db_session.expire_all()
    db_todo = db_session.query(TodoDB).filter_by(id=deleted_id).first()
    assert db_todo is None
    count = db_session.query(TodoDB).filter_by(id=deleted_id).count()
    assert count == 0

    allure.attach(
        '<table border="1" style="border-collapse: collapse; width: 100%;">'
        '<tr style="background-color: #f2f2f2;"><th style="padding: 8px; text-align: left;">Assertion</th><th style="padding: 8px; text-align: left;">Forventet</th></tr>'
        '<tr><td style="padding: 8px;">response.elapsed.total_seconds() &lt; 2</td><td style="padding: 8px;">REQ-012: Svartid under 2 sekunder</td></tr>'
        '<tr><td style="padding: 8px;">"application/json" in Content-Type</td><td style="padding: 8px;">REQ-014: Response er JSON format</td></tr>'
        '<tr><td style="padding: 8px;">db_todo_before is not None</td><td style="padding: 8px;">REQ-015: Rækken eksisterede inden sletning</td></tr>'
        '<tr><td style="padding: 8px;">deleted_id &gt; 0</td><td style="padding: 8px;">REQ-004: ID var positivt</td></tr>'
        '<tr><td style="padding: 8px;">db_todo is None</td><td style="padding: 8px;">REQ-008: Rækken er slettet fra databasen</td></tr>'
        '<tr><td style="padding: 8px;">count == 0</td><td style="padding: 8px;">Query returnerer nul rækker</td></tr>'
        "</table>",
        name="Database assertions",
        attachment_type=allure.attachment_type.HTML
    )
    allure.attach(delete_equivalence_table("K1"), name="Testdesign", attachment_type=allure.attachment_type.HTML)
    allure.attach(delete_diagram(deleted_id), name="Flow Diagram", attachment_type=allure.attachment_type.HTML)
    _link_reqs("REQ-004", "REQ-008", "REQ-012", "REQ-013", "REQ-014", "REQ-015")


@pytest.mark.regression
@pytest.mark.negative
@allure.feature("001_Tests")
@allure.story("001D_DELETE")
@allure.title("Slet todo der ikke findes")
@allure.description("Beskrivelse: Forsøger at slette en todo med et id der ikke eksisterer\nForventet: HTTP 404")
def test_slet_todo_der_ikke_findes(db_session):
    """
    Testdesign: Negativ test
    Beskrivelse: Forsøger at slette en todo med et id der ikke eksisterer
    Forudsætning: Todo med id 99999 eksisterer ikke i API'et
    Forventet resultat: HTTP 404
    """
    db_todo = db_session.query(TodoDB).filter_by(id=99999).first()
    assert db_todo is None

    response = requests.delete(f"{BASE_URL}/todos/99999")
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
    allure.attach(delete_equivalence_table("K3"), name="Testdesign", attachment_type=allure.attachment_type.HTML)
    allure.attach(negative_delete_diagram(99999), name="Flow Diagram", attachment_type=allure.attachment_type.HTML)
    _link_reqs("REQ-008", "REQ-009", "REQ-012", "REQ-013")


@pytest.mark.regression
@allure.feature("001_Tests")
@allure.story("001D_DELETE")
@allure.title("Valider tomt response ved DELETE")
@allure.description(
    "Beskrivelse: Validerer at response ved DELETE er et tomt objekt<br>"
    "Forventet: HTTP 200 og response body er {}"
)
def test_valider_tomt_response(new_todo, db_session):
    """
    Testdesign: Ækvivalenspartitionering
    Beskrivelse: Validerer at response ved DELETE er et tomt objekt
    Forudsætning: Todo eksisterer i API'et
    Forventet resultat: HTTP 200 og response body er {}
    """
    created = requests.post(f"{BASE_URL}/todos", json=new_todo).json()
    deleted_id = created["id"]

    db_todo_before = db_session.query(TodoDB).filter_by(id=deleted_id).first()
    assert db_todo_before is not None

    response = requests.delete(f"{BASE_URL}/todos/{deleted_id}")
    assert response.status_code == 200
    assert response.elapsed.total_seconds() < 2
    assert response.json() == {}

    db_session.expire_all()
    db_todo = db_session.query(TodoDB).filter_by(id=deleted_id).first()
    assert db_todo is None
    count = db_session.query(TodoDB).filter_by(id=deleted_id).count()
    assert count == 0

    allure.attach(
        '<table border="1" style="border-collapse: collapse; width: 100%;">'
        '<tr style="background-color: #f2f2f2;"><th style="padding: 8px; text-align: left;">Assertion</th><th style="padding: 8px; text-align: left;">Forventet</th></tr>'
        '<tr><td style="padding: 8px;">response.elapsed.total_seconds() &lt; 2</td><td style="padding: 8px;">REQ-012: Svartid under 2 sekunder</td></tr>'
        '<tr><td style="padding: 8px;">db_todo_before is not None</td><td style="padding: 8px;">REQ-015: Rækken eksisterede inden sletning</td></tr>'
        '<tr><td style="padding: 8px;">deleted_id &gt; 0</td><td style="padding: 8px;">REQ-004: ID var positivt</td></tr>'
        '<tr><td style="padding: 8px;">db_todo is None</td><td style="padding: 8px;">REQ-008: Rækken er slettet fra databasen</td></tr>'
        '<tr><td style="padding: 8px;">count == 0</td><td style="padding: 8px;">Query returnerer nul rækker</td></tr>'
        "</table>",
        name="Database assertions",
        attachment_type=allure.attachment_type.HTML
    )
    allure.attach(delete_equivalence_table("K2"), name="Testdesign", attachment_type=allure.attachment_type.HTML)
    allure.attach(delete_diagram(deleted_id), name="Flow Diagram", attachment_type=allure.attachment_type.HTML)
    _link_reqs("REQ-004", "REQ-008", "REQ-012", "REQ-013", "REQ-015")
