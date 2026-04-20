import allure


@allure.epic("002_E2E")
@allure.feature("002A_Flows")
@allure.story("E2E Beslutningsflows")
@allure.title("E2E Beslutningsflows — Todo App")
@allure.description(
    "Beskrivelse: Viser E2E beslutningsflows for Todo App<br>"
    "Forventet: Diagram vises i Allure rapporten"
)
def test_e2e_flows():
    allure.attach(
        "E2E flows kommer snart",
        name="E2E Beslutningsflows",
        attachment_type=allure.attachment_type.TEXT,
    )