import allure

from tests.todo_api.diagrams_e2e import e2e_diagram


@allure.epic("002_E2E")
@allure.feature("002A_Flows")
@allure.story("E2E Beslutningsflows")
@allure.title("E2E Beslutningsflows — Todo App")
@allure.description(
    "Beskrivelse: Viser E2E beslutningsflows for autentificering, Todo CRUD og logout<br>"
    "Forventet: SVG diagram vises korrekt i Allure rapporten"
)
def test_e2e_flows():
    allure.attach(
        e2e_diagram(),
        name="E2E Beslutningsflows",
        attachment_type=allure.attachment_type.HTML,
    )
