import pytest
import allure
import requests
from tests.todo_api.conftest import BASE_URL
from api.models_db import TodoDB
from tests.todo_api.diagrams import delete_diagram, negative_delete_diagram
from tests.todo_api.testdesign_tables import delete_equivalence_table


@pytest.mark.smoke
@pytest.mark.regression
@allure.feature("Todo API")
@allure.story("DELETE")
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

    db_session.expire_all()
    db_todo = db_session.query(TodoDB).filter_by(id=deleted_id).first()
    assert db_todo is None
    count = db_session.query(TodoDB).filter_by(id=deleted_id).count()
    assert count == 0

    allure.attach(
        '<table border="1" style="border-collapse: collapse; width: 100%;">'
        '<tr style="background-color: #f2f2f2;"><th style="padding: 8px; text-align: left;">Assertion</th><th style="padding: 8px; text-align: left;">Forventet</th></tr>'
        '<tr><td style="padding: 8px;">db_todo_before is not None</td><td style="padding: 8px;">Rækken eksisterede inden sletning</td></tr>'
        '<tr><td style="padding: 8px;">deleted_id > 0</td><td style="padding: 8px;">ID var positivt</td></tr>'
        '<tr><td style="padding: 8px;">db_todo is None</td><td style="padding: 8px;">Rækken er slettet fra databasen</td></tr>'
        '<tr><td style="padding: 8px;">count == 0</td><td style="padding: 8px;">Query returnerer nul rækker</td></tr>'
        "</table>",
        name="Database assertions",
        attachment_type=allure.attachment_type.HTML
    )

    allure.attach(delete_equivalence_table("K1"), name="Testdesign", attachment_type=allure.attachment_type.HTML)
    allure.attach(delete_diagram(deleted_id), name="Flow Diagram", attachment_type=allure.attachment_type.HTML)


@pytest.mark.regression
@pytest.mark.negative
@allure.feature("Todo API")
@allure.story("DELETE")
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

    allure.attach(
        '<table border="1" style="border-collapse: collapse; width: 100%;">'
        '<tr style="background-color: #f2f2f2;"><th style="padding: 8px; text-align: left;">Assertion</th><th style="padding: 8px; text-align: left;">Forventet</th></tr>'
        '<tr><td style="padding: 8px;">db_todo is None</td><td style="padding: 8px;">ID 99999 eksisterer ikke i databasen</td></tr>'
        '<tr><td style="padding: 8px;">response.status_code == 404</td><td style="padding: 8px;">HTTP 404</td></tr>'
        "</table>",
        name="Database assertions",
        attachment_type=allure.attachment_type.HTML
    )

    allure.attach(delete_equivalence_table("K3"), name="Testdesign", attachment_type=allure.attachment_type.HTML)
    allure.attach(negative_delete_diagram(99999), name="Flow Diagram", attachment_type=allure.attachment_type.HTML)


@pytest.mark.regression
@allure.feature("Todo API")
@allure.story("DELETE")
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
    assert response.json() == {}

    db_session.expire_all()
    db_todo = db_session.query(TodoDB).filter_by(id=deleted_id).first()
    assert db_todo is None
    count = db_session.query(TodoDB).filter_by(id=deleted_id).count()
    assert count == 0

    allure.attach(
        '<table border="1" style="border-collapse: collapse; width: 100%;">'
        '<tr style="background-color: #f2f2f2;"><th style="padding: 8px; text-align: left;">Assertion</th><th style="padding: 8px; text-align: left;">Forventet</th></tr>'
        '<tr><td style="padding: 8px;">db_todo_before is not None</td><td style="padding: 8px;">Rækken eksisterede inden sletning</td></tr>'
        '<tr><td style="padding: 8px;">deleted_id > 0</td><td style="padding: 8px;">ID var positivt</td></tr>'
        '<tr><td style="padding: 8px;">db_todo is None</td><td style="padding: 8px;">Rækken er slettet fra databasen</td></tr>'
        '<tr><td style="padding: 8px;">count == 0</td><td style="padding: 8px;">Query returnerer nul rækker</td></tr>'
        "</table>",
        name="Database assertions",
        attachment_type=allure.attachment_type.HTML
    )

    allure.attach(delete_equivalence_table("K2"), name="Testdesign", attachment_type=allure.attachment_type.HTML)
    allure.attach(delete_diagram(deleted_id), name="Flow Diagram", attachment_type=allure.attachment_type.HTML)
