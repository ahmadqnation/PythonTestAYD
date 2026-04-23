# PythonTestAYD — Automationstest Suite

Et testprojekt der dækker API-tests, E2E-tests og load tests for en Todo-applikation med authentication og CVR-opslag.

## Projektbeskrivelse

Projektet tester en fuld Todo-applikation bestående af en REST API, en frontend og en Mock CVR API. Testsuiten er bygget med fokus på systematisk testdesign via ækvivalenspartitionering, grænseværdianalyse og negative tests.

**Hvad der testes:**

- **JSONPlaceholder API** — Offentlig mock-API til test af CRUD-operationer (posts, users, todos, comments)
- **Todo API** — Brugerdefineret REST API med JWT-authentication og PostgreSQL-database
- **Frontend** — React-baseret Todo-applikation med login, registrering og CVR-opslag
- **Mock CVR API** — Lokal FastAPI-service der simulerer CVR-opslag ved registrering

**Testdesign-teknikker:**

- Ækvivalenspartitionering
- Grænseværdianalyse
- Negative tests (4xx-fejlscenarier)
- E2E-workflows

---

## Live URLs

| Service | URL |
|---------|-----|
| Todo API | https://pythonayd-todo-api.onrender.com |
| Mock CVR API | https://pythonayd-mock-cvr.onrender.com/docs |
| Frontend | https://ahmadqnation.github.io/PythonTestAYD/app |
| GitHub | https://github.com/ahmadqnation/PythonTestAYD |

---

## Installation

### Python (pytest + Locust)

```bash
pip install -r requirements.txt
```

### Node.js (Cypress)

```bash
npm install
```

### Mock CVR API (lokal)

```bash
pip install -r mock_cvr/requirements.txt
uvicorn mock_cvr.main:app --reload --port 8000
```

---

## Pytest API Tests

Tests er opdelt i to kategorier: tests mod det offentlige JSONPlaceholder API og tests mod det brugerdefinerede Todo API.

### Test-filer

#### JSONPlaceholder API (`tests/`)

| Fil | Endpoint | Metoder |
|-----|----------|---------|
| `tests/posts/test_get.py` | `/posts`, `/posts/{id}`, `/posts/{id}/comments` | GET |
| `tests/posts/test_post.py` | `/posts` | POST |
| `tests/posts/test_put.py` | `/posts/{id}` | PUT |
| `tests/posts/test_delete.py` | `/posts/{id}` | DELETE |
| `tests/users/test_get.py` | `/users`, `/users/{id}`, `/users/{id}/posts` | GET |
| `tests/todos/test_get.py` | `/todos`, `/todos/{id}` | GET |
| `tests/comments/test_get.py` | `/comments` | GET |

#### Todo API (`tests/todo_api/`)

| Fil | Fokus |
|-----|-------|
| `test_get.py` | GET `/todos` og `/todos/{id}` med database-assertions |
| `test_post.py` | POST `/todos` med authentication |
| `test_put.py` | PUT `/todos/{id}` |
| `test_delete.py` | DELETE `/todos/{id}` |
| `test_e2e_overview.py` | Fuld CRUD-workflow end-to-end |

### Test markers

| Marker | Beskrivelse |
|--------|-------------|
| `smoke` | Kritiske core-tests |
| `regression` | Fuld regressionstest |
| `negative` | Fejlhåndtering og ugyldige inputs |

### Køre pytest tests

```bash
# Alle tests
pytest

# Filtrér på marker
pytest -m smoke
pytest -m regression
pytest -m negative

# Kun Todo API tests
pytest tests/todo_api/

# Via run_tests.py
python run_tests.py
python run_tests.py smoke
python run_tests.py regression
```

### Testrapporter

```bash
# Åbn HTML-rapport
open reports/report.html

# Generér og åbn Allure-rapport
allure serve reports/allure-results
```

---

## Cypress E2E Tests

E2E-tests kører mod den live frontend og bruger Page Object Model (POM) med mocked API-kald.

### Test-filer

| Fil | Test cases | Hvad testes |
|-----|-----------|-------------|
| `cypress/e2e/auth/login.cy.js` | TC-AUTH-001 til TC-AUTH-004 | Login-flow, redirect, token-lagring |
| `cypress/e2e/auth/register.cy.js` | TC-AUTH-005 til TC-AUTH-007 | Registrering med CVR-opslag |
| `cypress/e2e/auth/logout.cy.js` | — | Logout og session-rydning |
| `cypress/e2e/todos/create.cy.js` | TC-TODO-001 til TC-TODO-002 | Opret todo, valideringsblokering |
| `cypress/e2e/todos/update.cy.js` | — | Opdater todo |
| `cypress/e2e/todos/delete.cy.js` | TC-TODO-005 | Slet todo og fjern fra liste |
| `cypress/e2e/non_functional/nfr.cy.js` | TC-NFR-001 til TC-NFR-005 | Svartider, HTTPS, JWT-sikkerhed |

### Køre Cypress tests

```bash
# Åbn interaktiv Test Runner (UI)
npx cypress open

# Kør alle tests i headless mode
npx cypress run

# Kør specifikke tests
npx cypress run --spec "cypress/e2e/auth/*"
npx cypress run --spec "cypress/e2e/todos/*"

# Kør med specifik browser
npx cypress run --browser chrome
npx cypress run --browser firefox

# Kør i alle browsere
node cypress/runners/run-all-browsers.js
```

---

## Locust Load Tests

Projektet indeholder 4 typer load tests implementeret med [Locust](https://locust.io/). Alle tests logger ind med `locust@test.dk` og tester `/todos`-endpointet.

### Installation

```bash
pip install locust
```

### Opret testbruger (kun første gang)

```bash
python locust/create_locust_user.py
```

### Test typer og kommandoer

#### 1. Standard load test (`locustfile.py`)

Grundlæggende load test. Konfigureres manuelt via Locust-webgrænsefladen med ønsket antal brugere og spawn rate.

```bash
locust -f locust/locustfile.py --host https://pythonayd-todo-api.onrender.com
```

#### 2. Spike test (`locustfile_spike.py`)

Simulerer en pludselig trafikstigning op til 200 samtidige brugere på 10 sekunder, efterfulgt af fald tilbage til normalt. Varighed: ~110 sek.

| Fase | Brugere | Varighed |
|------|---------|----------|
| Opvarmning | 10 | 30 sek |
| Spike | 200 | 10 sek |
| Hold spike | 200 | 30 sek |
| Fald | 10 | 10 sek |
| Stabilisering | 10 | 30 sek |

```bash
locust -f locust/locustfile_spike.py --host https://pythonayd-todo-api.onrender.com
```

#### 3. Endurance test (`locustfile_endurance.py`)

Tester systemets stabilitet over tid med konstant belastning i 30 minutter. Varighed: ~32 min.

| Fase | Brugere | Varighed |
|------|---------|----------|
| Opvarmning | 20 | 60 sek |
| Udholdenhed | 20 | 30 min |
| Nedlukning | 0 | 60 sek |

```bash
locust -f locust/locustfile_endurance.py --host https://pythonayd-todo-api.onrender.com
```

#### 4. Step/Shape test (`locustfile_shape.py`)

Trinvis øgning af belastning for at finde systemets grænser. Varighed: ~10 min.

| Fase | Brugere | Varighed |
|------|---------|----------|
| Trin 1 | 10 | 2 min |
| Trin 2 | 25 | 2 min |
| Trin 3 | 50 | 2 min |
| Trin 4 | 100 | 2 min |
| Trin 5 | 150 | 2 min |

```bash
locust -f locust/locustfile_shape.py --host https://pythonayd-todo-api.onrender.com
```

### Webgrænseflade

Alle tests starter en webgrænseflade på `http://localhost:8089` — åbn den i browseren for at starte og monitorere testen. Tests med `LoadTestShape` (spike, endurance, step) starter automatisk uden manuel konfiguration.
