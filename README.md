# 🐴 Horse Owner

A Web Application designed to help riders look after their horses and plan and analyse their trainings sessions.
Based on MVP version.

## 0. Podstawowa struktura projektu

Projekt zainicjowany z płaską strukturą katalogów, oparty o framework Django z naciskiem na skalowalność i gotowość do pracy w różnych środowiskach (Development, Test, Production).

```text
Horse_Owner
├── .gitignore               # Wykluczenia plików środowiskowych i systemowych
├── docker-compose.yml       # Konfiguracja infrastruktury (lokalna baza PostgreSQL)
├── manage.py                # Skrypt zarządzający (zmodyfikowany pod ustawienia lokalne)
├── pytest.ini               # Punkt wejścia dla testów (wskazuje na ustawienia testowe)
├── README.md                # Dokumentacja projektu
├── requirements.txt         # Zamrożone pakiety (Django, pytest, psycopg)
└── horse_owner/             # Główny moduł konfiguracyjny aplikacji
    ├── __init__.py
    ├── asgi.py
    ├── urls.py
    ├── wsgi.py
    └── settings/            # Modułowa architektura ustawień
        ├── __init__.py
        ├── base.py          # Rdzeń ustawień współdzielony przez wszystkie środowiska
        ├── local.py         # Środowisko developerskie (podpięty PostgreSQL z Dockera)
        └── test.py          # Środowisko testowe (szybka baza in-memory SQLite, MD5Hasher)
```

Kluczowe założenia początkowe:
- Modułowe ustawienia: Zamiast jednego, spuchniętego pliku settings.py, konfiguracja została rozbita na pakiet settings/. Zapewnia to separację danych wrażliwych i optymalizację środowiska pod konkretny cel.

- Baza danych: Środowisko lokalne wykorzystuje silnik PostgreSQL 15 postawiony w kontenerze Dockera, aby maksymalnie zbliżyć się do warunków produkcyjnych. Z kolei środowisko testowe w test.py jest nadpisane na in-memory SQLite w celu ekstremalnego przyspieszenia wykonywania testów.

- TDD (Test-Driven Development): Projekt jest skonfigurowany pod rygorystyczne testowanie logiki za pomocą narzędzi pytest oraz pytest-django.