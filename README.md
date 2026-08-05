# 🐴 Horse Owner

A web application for managing horse care, training records and preventive health
scheduling, with an AI assistant that analyses training history and answers questions about
it.

> 🚧 **In active development.** The application is being built test-first — see
> [Development approach](#development-approach) below. An earlier Flask prototype lives in
> [Mission-AIpossible](https://github.com/TomaszLitwicki/Mission-AIpossible/tree/main/HorseOwner).

---

## Why this project

I ran a horse training centre for nine years. Care schedules, vaccination dates, farrier
visits and training notes were spread across notebooks, phone photos and memory — and the
cost of forgetting one of them is a vet bill or an injured animal.

The domain knowledge here is first-hand, which makes it a good project to build properly:
I know what the data should look like, what questions an owner actually asks, and where an
AI assistant helps rather than gets in the way.

---

## Planned features

| Module | What it covers |
| :-- | :-- |
| **Accounts** | Registration, login, per-user dashboard |
| **Horses** | Profiles — name, breed, age, colour, chip number, notes, photo |
| **Trainings** | Session log with date, type, duration, intensity and notes |
| **Care** | Vaccinations, farrier visits, dental care, deworming, with due-date tracking |
| **Contacts** | Vet, farrier, physiotherapist, transport |
| **AI assistant** | Analyses recent training history and answers questions about it |

### AI assistant boundaries

The assistant works from the horse's own training data and is explicitly instructed **not to
give medical or diagnostic advice**. In a domain where bad guidance harms an animal that
cannot object, the useful design decision is deciding what the model must refuse to do.

---

## Tech stack

| Layer | Technology |
| :-- | :-- |
| Backend | Python 3.14, Django 6 |
| Database | PostgreSQL 15 (`psycopg` 3) |
| Environment | Docker Compose — database service |
| Testing | pytest, pytest-django, pytest-cov, Selenium |
| AI | OpenAI API, prompt engineering |
| Frontend | Django templates, HTML, CSS |

### Settings layout

Settings are split by environment rather than kept in one file:

```
horse_owner/settings/
├─ base.py     shared configuration, secrets read from the environment
├─ local.py    development — PostgreSQL in Docker
└─ test.py     test runs — in-memory SQLite, fast password hashing
```

The test configuration deliberately swaps PostgreSQL for in-memory SQLite and the default
password hasher for MD5. Neither belongs anywhere near production, and both exist for one
reason: a test suite that runs in seconds is a suite you actually run on every change.

---

## Development approach

The application is built **test-first**. For each feature:

1. A failing test is written that describes the expected behaviour.
2. The minimum code to pass it is implemented.
3. The implementation is refactored with the test as a safety net.

Commit history reflects this order — test commits precede the implementation they cover.
The testing stack was configured before the first view was written, which is the point:
the tests are not something added at the end.

### Test layers

**Unit and integration** (`pages/tests.py`) — views, routing, forms and authentication flow,
exercised through Django's test client. Negative paths are covered alongside the happy ones:
mismatched passwords, duplicate usernames, and access to protected pages after logout.

**End-to-end** (`functional_tests/`) — full user journeys driven through a real browser with
Selenium. Page elements are wrapped in a **Page Object**, so a change to a template's markup
is fixed in one place rather than across every test that touches it.

```bash
pytest                # all tests
pytest --cov          # with coverage report
```

---

## Getting started

Requires Python 3.14, Docker, and Firefox with geckodriver for the browser tests.

```bash
git clone https://github.com/TomaszLitwicki/Horse_Owner.git
cd Horse_Owner

python -m venv .venv
source .venv/bin/activate          # Windows: .\.venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env               # then fill in the values
docker compose up -d               # starts PostgreSQL

python manage.py migrate
python manage.py runserver
```

The application starts on `http://127.0.0.1:8000`.

Generate a secret key for `.env` with:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Environment variables

| Variable | Purpose |
| :-- | :-- |
| `DJANGO_SECRET_KEY` | Django session and cryptographic signing |
| `DJANGO_DEBUG` | `True` in development, `False` otherwise |
| `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD` | Database credentials |
| `POSTGRES_HOST`, `POSTGRES_PORT` | Database location — `127.0.0.1:5432` with the bundled Compose file |
| `OPENAI_API_KEY` | AI assistant; the app runs without it, with the assistant disabled |

A single `.env` file in the project root serves both Django and Docker Compose.

---

## Status

**Done**
- [x] Django project scaffolding
- [x] Environment-split settings — base / local / test
- [x] Secrets and database credentials read from the environment
- [x] PostgreSQL 15 in Docker Compose, with a persistent volume
- [x] pytest configured with pytest-django and coverage
- [x] Accounts — registration, login, logout, protected dashboard
- [x] End-to-end browser tests with a Page Object layer

**In progress**
- [ ] Horses module — models, views, tests
- [ ] Trainings module
- [ ] Care module — events and due-date tracking
- [ ] Contacts module
- [ ] AI assistant — training analysis

**Planned**
- [ ] Containerising the application alongside the database
- [ ] Continuous integration — test suite on every push
- [ ] Progress charts
- [ ] CSV / PDF export
- [ ] Due-date reminders
- [ ] Deployment

---

## Design

Colours drawn from a stable yard: Stable Green `#5E7B5B`, Hay Beige `#E9DFC8`, Saddle Brown
`#6B4E3D`, Fence Light `#F7F7F7`. Merriweather for headings, Roboto for body text.
Responsive across desktop and mobile.

The interface is in Polish; the codebase, tests and documentation are in English.

---

Built by [Tomasz Litwicki](https://github.com/TomaszLitwicki)