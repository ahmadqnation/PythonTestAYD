_TABLE_STYLE = "border-collapse: collapse; width: 100%; font-family: Arial, sans-serif; font-size: 13px;"
_HEADER_ROW_STYLE = "background-color: #f2f2f2;"
_TESTED_ROW_STYLE = "background-color: #d4edda;"
_TH_STYLE = "padding: 8px; text-align: left; border: 1px solid #dee2e6;"
_TD_STYLE = "padding: 8px; text-align: left; border: 1px solid #dee2e6;"
_TITLE_STYLE = (
    "font-family: Arial, sans-serif; font-size: 14px; "
    "font-weight: bold; color: #1E293B; margin: 0 0 8px 0;"
)


def _build_table(title: str, rows: list, tested_class: str) -> str:
    header = (
        f'<h3 style="{_TITLE_STYLE}">{title}</h3>'
        f'<table border="1" style="{_TABLE_STYLE}">'
        f'<tr style="{_HEADER_ROW_STYLE}">'
        f'<th style="{_TH_STYLE}">Klasse</th>'
        f'<th style="{_TH_STYLE}">Input</th>'
        f'<th style="{_TH_STYLE}">Forventet</th>'
        f'<th style="{_TH_STYLE}">Testes</th>'
        f'</tr>'
    )
    body = ""
    for (klasse, input_val, forventet, class_id) in rows:
        is_tested = class_id == tested_class
        row_style = f' style="{_TESTED_ROW_STYLE}"' if is_tested else ""
        testes = "✅" if is_tested else ""
        body += (
            f'<tr{row_style}>'
            f'<td style="{_TD_STYLE}">{klasse}</td>'
            f'<td style="{_TD_STYLE}">{input_val}</td>'
            f'<td style="{_TD_STYLE}">{forventet}</td>'
            f'<td style="{_TD_STYLE}">{testes}</td>'
            f"</tr>"
        )
    table = header + body + "</table>"
    return f'<html><body style="margin:0;padding:20px;background:#fff;">{table}</body></html>'


def post_equivalence_table(tested_class: str) -> str:
    rows = [
        ("K1 — Gyldig todo (alle felter)", "title + completed=False", "HTTP 201", "K1"),
        ("K2 — Gyldig todo (kun title, default completed)", "title (completed udeladt)", "HTTP 201", "K2"),
        ("K3 — Gyldig todo (completed=true)", "title + completed=True", "HTTP 201", "K3"),
        ("K4 — Manglende title (ugyldig)", "completed=False (ingen title)", "HTTP 422", "K4"),
    ]
    return _build_table(
        "Testdesign: Ækvivalenspartitionering — POST /todos",
        rows,
        tested_class,
    )


def put_equivalence_table(tested_class: str) -> str:
    rows = [
        ("K1 — Opdater title", 'id + title="Opdateret titel"', "HTTP 200", "K1"),
        ("K2 — Opdater completed", "id + completed=True", "HTTP 200", "K2"),
        ("K3 — Tomt objekt (ingen ændringer)", "id + {}", "HTTP 200", "K3"),
        ("K4 — Ikke-eksisterende id (ugyldig)", "id=99999", "HTTP 404", "K4"),
    ]
    return _build_table(
        "Testdesign: Ækvivalenspartitionering — PUT /todos",
        rows,
        tested_class,
    )


def delete_equivalence_table(tested_class: str) -> str:
    rows = [
        ("K1 — Slet eksisterende todo", "id (gyldigt)", "HTTP 200", "K1"),
        ("K2 — Tomt response ved sletning", "id (gyldigt)", "HTTP 200, body={}", "K2"),
        ("K3 — Ikke-eksisterende id (ugyldig)", "id=99999", "HTTP 404", "K3"),
    ]
    return _build_table(
        "Testdesign: Ækvivalenspartitionering — DELETE /todos",
        rows,
        tested_class,
    )


def get_equivalence_table(tested_class: str) -> str:
    rows = [
        ("K1 — Hent alle todos", "/todos", "HTTP 200, liste > 0", "K1"),
        ("K2 — Hent enkelt todo (gyldigt id)", "id (gyldigt int > 0)", "HTTP 200", "K2"),
        ("K3 — Valider felter i response", "id (gyldigt)", "HTTP 200, id+title+completed", "K3"),
        ("K4 — Ikke-eksisterende id (ugyldig)", "id=99999", "HTTP 404", "K4"),
        ("K5 — Negativt id (grænseværdi)", "id=-1", "HTTP 404", "K5"),
        ("K6 — Ugyldigt id-type (ugyldig)", 'id="abc"', "HTTP 422", "K6"),
    ]
    return _build_table(
        "Testdesign: Ækvivalenspartitionering — GET /todos",
        rows,
        tested_class,
    )


def post_boundary_table(tested_class: str) -> str:
    rows = [
        ("BV1 — Under nedre grænse (0 tegn)", 'title=""', "HTTP 422", "BV1"),
        ("BV2 — Nedre grænse (1 tegn)", 'title="a"', "HTTP 201", "BV2"),
        ("BV3 — Øvre grænse (500 tegn)", 'title="a" × 500', "HTTP 201", "BV3"),
        ("BV4 — Over øvre grænse (501 tegn)", 'title="a" × 501', "HTTP 422", "BV4"),
    ]
    return _build_table(
        "Testdesign: Grænseværdianalyse — POST /todos (title længde)",
        rows,
        tested_class,
    )
