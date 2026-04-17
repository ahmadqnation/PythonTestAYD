import allure

_GET    = "001_Tests/001A_GET"
_POST   = "001_Tests/001B_POST"
_PUT    = "001_Tests/001C_PUT"
_DELETE = "001_Tests/001D_DELETE"


def _links(*tests):
    """Build comma-separated plain-text test names."""
    return ", ".join(name for _, name in tests)


@allure.feature("000_Kravsoversigt")
@allure.story("Kravsoversigt")
@allure.title("Kravsoversigt — Todo API")
@allure.description(
    "Beskrivelse: Viser kravsoversigt for Todo API<br>"
    "Forventet: Alle krav er dokumenteret og opfyldt"
)
def test_kravsoversigt():
    """
    Kravsoversigt for Todo API — funktionelle og non-funktionelle krav
    """
    # (krav_id, beskrivelse, krav_type, prioritet, testcases_html)
    funktionelle = [
        (
            "REQ-001", "Title skal have minimum 1 tegn", "Funktionel", "Høj",
            _links(
                (_POST, "test_opret_todo_med_tom_titel"),
                (_POST, "test_opret_todo_med_enkelt_tegn"),
            ),
        ),
        (
            "REQ-002", "Title skal have maximum 500 tegn", "Funktionel", "Høj",
            _links(
                (_POST, "test_opret_todo_med_lang_titel"),
                (_POST, "test_opret_todo_over_max_laengde"),
            ),
        ),
        (
            "REQ-003", "Completed skal være boolean (true/false)", "Funktionel", "Høj",
            _links(
                (_POST, "test_opret_todo"),
                (_POST, "test_opret_todo_med_completed_true"),
                (_PUT,  "test_opdater_todo_completed"),
            ),
        ),
        (
            "REQ-004", "ID genereres automatisk og er unikt og positivt", "Funktionel", "Høj",
            _links(
                (_POST,   "test_opret_todo"),
                (_PUT,    "test_opdater_todo_titel"),
                (_DELETE, "test_slet_todo"),
            ),
        ),
        (
            "REQ-005", "GET /todos returnerer HTTP 200 og liste med todos", "Funktionel", "Høj",
            _links(
                (_GET, "test_hent_alle_todos"),
                (_GET, "test_hent_enkelt_todo"),
            ),
        ),
        (
            "REQ-006", "POST /todos returnerer HTTP 201 og opretter todo", "Funktionel", "Høj",
            _links(
                (_POST, "test_opret_todo"),
            ),
        ),
        (
            "REQ-007", "PUT /todos/{id} returnerer HTTP 200 og opdaterer todo", "Funktionel", "Høj",
            _links(
                (_PUT, "test_opdater_todo_titel"),
                (_PUT, "test_opdater_todo_completed"),
            ),
        ),
        (
            "REQ-008", "DELETE /todos/{id} returnerer HTTP 200 og sletter todo", "Funktionel", "Høj",
            _links(
                (_DELETE, "test_slet_todo"),
                (_DELETE, "test_valider_tomt_response"),
            ),
        ),
        (
            "REQ-009", "Ugyldigt id returnerer HTTP 404", "Funktionel", "Høj",
            _links(
                (_GET,    "test_hent_todo_der_ikke_findes"),
                (_PUT,    "test_opdater_todo_der_ikke_findes"),
                (_DELETE, "test_slet_todo_der_ikke_findes"),
            ),
        ),
        (
            "REQ-010", "Tom title returnerer HTTP 422", "Funktionel", "Høj",
            _links(
                (_POST, "test_opret_todo_med_tom_titel"),
            ),
        ),
        (
            "REQ-011", "Title over 500 tegn returnerer HTTP 422", "Funktionel", "Høj",
            _links(
                (_POST, "test_opret_todo_over_max_laengde"),
            ),
        ),
    ]

    non_funktionelle = [
        (
            "REQ-012", "API'et skal svare inden for 2 sekunder", "Non-funktionel", "Medium",
            _links(
                (_POST,   "test_post.py (alle)"),
                (_PUT,    "test_put.py (alle)"),
                (_DELETE, "test_delete.py (alle)"),
                (_GET,    "test_get.py (alle)"),
            ),
        ),
        (
            "REQ-013", "API'et skal understøtte HTTPS", "Non-funktionel", "Høj",
            _links(
                (_POST,   "test_post.py (alle)"),
                (_PUT,    "test_put.py (alle)"),
                (_DELETE, "test_delete.py (alle)"),
                (_GET,    "test_get.py (alle)"),
            ),
        ),
        (
            "REQ-014", "API'et skal returnere JSON format", "Non-funktionel", "Høj",
            _links(
                (_POST,   "test_opret_todo"),
                (_PUT,    "test_opdater_todo_titel"),
                (_PUT,    "test_opdater_todo_completed"),
                (_DELETE, "test_slet_todo"),
                (_GET,    "test_hent_alle_todos"),
                (_GET,    "test_hent_enkelt_todo"),
                (_GET,    "test_valider_felter_i_todo"),
            ),
        ),
        (
            "REQ-015", "Databasen skal gemme data persistent", "Non-funktionel", "Høj",
            _links(
                (_POST,   "test_opret_todo"),
                (_PUT,    "test_opdater_todo_titel"),
                (_PUT,    "test_opdater_todo_completed"),
                (_DELETE, "test_slet_todo"),
                (_GET,    "test_hent_enkelt_todo"),
                (_GET,    "test_valider_felter_i_todo"),
            ),
        ),
    ]

    th_style = "padding: 8px; text-align: left; border: 1px solid #dee2e6;"
    td_style = "padding: 8px; text-align: left; border: 1px solid #dee2e6;"
    table_style = "border-collapse: collapse; width: 100%; font-family: Arial, sans-serif; font-size: 13px;"
    header_style = "background-color: #f2f2f2;"
    nf_row_style = " style=\"background-color: #f8f9fa;\""
    title_style = (
        "font-family: Arial, sans-serif; font-size: 14px; "
        "font-weight: bold; color: #1E293B; margin: 0 0 8px 0;"
    )

    rows = ""
    for (krav_id, beskrivelse, krav_type, prioritet, testcases) in funktionelle:
        rows += (
            f"<tr>"
            f'<td style="{td_style}">{krav_id}</td>'
            f'<td style="{td_style}">{beskrivelse}</td>'
            f'<td style="{td_style}">{krav_type}</td>'
            f'<td style="{td_style}">{prioritet}</td>'
            f'<td style="{td_style}">✅</td>'
            f'<td style="{td_style}">{testcases}</td>'
            f"</tr>"
        )

    for (krav_id, beskrivelse, krav_type, prioritet, testcases) in non_funktionelle:
        rows += (
            f'<tr{nf_row_style}>'
            f'<td style="{td_style}">{krav_id}</td>'
            f'<td style="{td_style}">{beskrivelse}</td>'
            f'<td style="{td_style}">{krav_type}</td>'
            f'<td style="{td_style}">{prioritet}</td>'
            f'<td style="{td_style}">✅</td>'
            f'<td style="{td_style}">{testcases}</td>'
            f"</tr>"
        )

    note_style = (
        "font-family: Arial, sans-serif; font-size: 13px; color: #1E293B; "
        "background: #fffbe6; border: 1px solid #ffe58f; border-radius: 4px; "
        "padding: 8px 12px; margin: 0 0 12px 0;"
    )
    note = (
        f'<p style="{note_style}">'
        "💡 Find testcases i Behaviors fanen under "
        "<strong>001_Tests → 001A_GET, 001B_POST, 001C_PUT, 001D_DELETE</strong>"
        "</p>"
    )

    tabel = (
        f'<h3 style="{title_style}">Kravsoversigt — Todo API</h3>'
        f"{note}"
        f'<table border="1" style="{table_style}">'
        f'<tr style="{header_style}">'
        f'<th style="{th_style}">Krav ID</th>'
        f'<th style="{th_style}">Beskrivelse</th>'
        f'<th style="{th_style}">Type</th>'
        f'<th style="{th_style}">Prioritet</th>'
        f'<th style="{th_style}">Status</th>'
        f'<th style="{th_style}">Testcases</th>'
        f"</tr>"
        f"{rows}"
        f"</table>"
    )

    allure.attach(
        f'<html><body style="margin:0;padding:20px;background:#fff;">{tabel}</body></html>',
        name="Kravsoversigt",
        attachment_type=allure.attachment_type.HTML
    )
