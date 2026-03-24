# FastAPI Testing with Pytest 

---

## 1. Pytest Setup

### What is Pytest?

Pytest is a Python testing framework. It finds functions that start with `test_`, runs them, and tells you which passed or failed. Simple.

### Installation

```bash
pip install pytest
pip install httpx          # Required by FastAPI's TestClient
pip install pytest-cov     # Optional: for code coverage reports
```

For your project specifically, you also need these already installed:
```bash
pip install fastapi sqlalchemy python-jose passlib[bcrypt]
```

### Running Tests

```bash
# Run all tests
pytest

# Run with verbose output (shows each test name)
pytest -v

# Run a specific file
pytest tests/test_auth.py

# Run a specific test function
pytest tests/test_auth.py::test_register_user

# Run with coverage report
pytest --cov=main --cov-report=term-missing
```

### Project Folder Structure

This is the recommended structure for your Employee Management project:

```
your_project/
│
├── main.py                  ← your FastAPI app
├── app.db                   ← production database (DO NOT touch in tests)
│
├── tests/
│   ├── __init__.py          ← makes 'tests' a Python package (can be empty)
│   ├── conftest.py          ← shared fixtures (explained below)
│   ├── test_auth.py         ← tests for register & login
│   ├── test_employees.py    ← tests for CRUD operations
│   └── test_dashboard.py    ← tests for dashboard endpoint
│
└── pytest.ini               ← pytest configuration (optional but useful)
```

### `pytest.ini` (optional but recommended)

Create this at your project root:

```ini
[pytest]
testpaths = tests
addopts = -v
```

This tells pytest: "look for tests inside the `tests/` folder" and always run in verbose mode.

---

## 2. Test Structure

### The AAA Pattern

Every test you write should follow this 3-step pattern:

```
Arrange  →  Act  →  Assert
(set up)    (do)    (check)
```

### Anatomy of a Test Function

```python
def test_something():
    # --- ARRANGE ---
    # Set up the data or state you need
    user_data = {"email": "test@test.com", "password": "secret"}

    # --- ACT ---
    # Call the thing you're testing
    response = client.post("/api/v1/login", data=user_data)

    # --- ASSERT ---
    # Check that the result is what you expected
    assert response.status_code == 200
    assert "access_token" in response.json()
```

### Naming Rules

| Rule | Example |
|------|---------|
| File must start with `test_` | `test_auth.py` ✅ |
| Function must start with `test_` | `test_register_user()` ✅ |
| Class (optional) must start with `Test` | `class TestAuth:` ✅ |

### Using Classes to Group Tests (Optional but Clean)

```python
class TestAuthentication:
    def test_register_success(self, client):
        ...

    def test_register_duplicate_email(self, client):
        ...

    def test_login_success(self, client):
        ...
```

Grouping by class makes output easier to read and lets you share setup via `setup_method`.

### Common Assertions

```python
# Status codes
assert response.status_code == 200
assert response.status_code == 201
assert response.status_code == 400
assert response.status_code == 404
assert response.status_code == 401

# Response body
data = response.json()
assert data["email"] == "test@example.com"
assert "access_token" in data
assert data["total_employs"] == 0

# Lists
assert len(data) == 3
assert data == []

# Types
assert isinstance(data["id"], int)
assert isinstance(data["isOnProject"], bool)
```

---

## 3. Fixtures

### What is a Fixture?

A fixture is a function that **prepares something** your test needs — like a database, a logged-in user, or sample data — and then **cleans it up** after the test is done.

Think of it like this:
- A restaurant sets the table before you arrive → **setup**
- They clean the table after you leave → **teardown**

### Basic Fixture Syntax

```python
import pytest

@pytest.fixture
def sample_user():
    return {
        "fullname": "John Doe",
        "email": "john@example.com",
        "password": "secret123"
    }

def test_something(sample_user):   # ← pytest automatically passes the fixture
    assert sample_user["email"] == "john@example.com"
```

### Fixture with Teardown using `yield`

`yield` is how you split a fixture into setup and teardown:

```python
@pytest.fixture
def database():
    # SETUP: runs before the test
    db = create_database()
    print("Database created")
    
    yield db          # ← test runs HERE, gets the db value
    
    # TEARDOWN: runs after the test (always, even if test fails)
    db.drop_all_tables()
    print("Database cleaned up")
```

### Fixture Scope

Scope controls **how often** a fixture is created and destroyed:

| Scope | Created | Destroyed | Use Case |
|-------|---------|-----------|----------|
| `function` (default) | Before each test | After each test | Fresh DB per test |
| `class` | Before first test in class | After last test in class | Shared state in a class |
| `module` | Once per file | After all tests in file | Expensive setups |
| `session` | Once per `pytest` run | At the very end | Shared read-only data |

```python
@pytest.fixture(scope="function")   # default
def fresh_db():
    ...

@pytest.fixture(scope="session")
def app_config():
    return {"debug": True}
```

For testing APIs with databases, **always use `scope="function"`** so each test gets a clean, isolated database.

### `conftest.py` — Sharing Fixtures Across Files

`conftest.py` is a special file that pytest automatically discovers. Any fixture defined in it is available to **all test files** in the same directory without importing.

```
tests/
├── conftest.py        ← fixtures here are available everywhere
├── test_auth.py       ← can use fixtures from conftest.py directly
└── test_employees.py  ← same here
```

### Fixtures Can Use Other Fixtures

```python
@pytest.fixture
def db_session():
    ...
    yield session

@pytest.fixture
def authenticated_client(db_session):  # ← uses db_session fixture
    # Create a test user
    user = create_user(db_session, email="test@test.com")
    token = get_token(user)
    client.headers = {"Authorization": f"Bearer {token}"}
    yield client
```

---

## 4. TestClient (FastAPI)

### What is TestClient?

FastAPI provides a `TestClient` (powered by `httpx`) that lets you make HTTP requests to your app **in memory**, without running a real server.

```python
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

response = client.get("/api/v1/dashboard")
print(response.status_code)   # 401
print(response.json())        # {"detail": "Not authenticated"}
```

No `uvicorn` needed. No port. Just `client.method(url)`.

### All HTTP Methods

```python
# GET
response = client.get("/api/v1/employs")

# POST with JSON body
response = client.post("/api/v1/employ", json={"fullname": "Alice", ...})

# POST with form data (used for login — OAuth2PasswordRequestForm)
response = client.post("/api/v1/login", data={"username": "a@b.com", "password": "pass"})
#                                        ^^^^ use `data=` NOT `json=` for form data

# PUT
response = client.put("/api/v1/employ/1", json={...})

# DELETE
response = client.delete("/api/v1/employ/1")
```

> **Important:** The login endpoint uses `OAuth2PasswordRequestForm` which reads `username` and `password` as **form fields**, not JSON. Always use `data=` for login.

### Sending Auth Headers

Most of your endpoints require a JWT token. Pass it in the `Authorization` header:

```python
headers = {"Authorization": f"Bearer {token}"}

response = client.get("/api/v1/dashboard", headers=headers)
response = client.get("/api/v1/employs", headers=headers)
response = client.post("/api/v1/employ", json={...}, headers=headers)
```

### Using TestClient as Context Manager

```python
with TestClient(app) as client:
    response = client.get("/api/v1/dashboard")
    # app startup/shutdown events are triggered
```

### TestClient + Override Dependencies (Testing with a Separate DB)

This is the most important pattern. You **don't want tests to touch your real `app.db`**. You override the database dependency to use a separate test database:

```python
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app, get_db, Base

# Use an in-memory SQLite database — fast, isolated, disappears after tests
TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Tell FastAPI: when anyone asks for `get_db`, give them `override_get_db` instead
app.dependency_overrides[get_db] = override_get_db
```

---
