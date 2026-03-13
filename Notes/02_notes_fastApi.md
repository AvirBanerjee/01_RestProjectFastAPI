# FastAPI  CRUD Application

---

# 📁 main.py 

```python
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker, Session


# DB Congig.


DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()

# DB MODEL


class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)

# Create tables
Base.metadata.create_all(bind=engine)


# Schemas


class UserCreate(BaseModel):
    name: str
    email: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True

# APP


app = FastAPI()


# CORS 


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# DB session


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# CRUD


# CREATE
@app.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate):
    db: Session = SessionLocal()
    db_user = UserDB(name=user.name, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    db.close()
    return db_user

# READ 
@app.get("/users/", response_model=List[UserResponse])
def get_users():
    db: Session = SessionLocal()
    users = db.query(UserDB).all()
    db.close()
    return users

# READ ONE
@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    db: Session = SessionLocal()
    user = db.query(UserDB).filter(UserDB.id == user_id).first()
    db.close()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# UPDATE
@app.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, updated_user: UserCreate):
    db: Session = SessionLocal()
    user = db.query(UserDB).filter(UserDB.id == user_id).first()

    if not user:
        db.close()
        raise HTTPException(status_code=404, detail="User not found")

    user.name = updated_user.name
    user.email = updated_user.email

    db.commit()
    db.refresh(user)
    db.close()

    return user

# DELETE
@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    db: Session = SessionLocal()
    user = db.query(UserDB).filter(UserDB.id == user_id).first()

    if not user:
        db.close()
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    db.close()

    return {"message": "User deleted successfully"}
```

---


## 1️⃣ Create Virtual Environment

```bash
python -m venv venv
```

### Activate it:

### Windows
```bash
venv\Scripts\activate
```

### Mac/Linux
```bash
source venv/bin/activate
```

---

## 2️⃣ Install Dependencies

```bash
pip install fastapi uvicorn sqlalchemy pydantic
```

---

## 3️⃣ Run the Server

```bash
uvicorn main:app --reload
```

You will see:

```
Uvicorn running on http://127.0.0.1:8000
```

---

## 4️⃣ Test API in Browser

Open:

```
http://127.0.0.1:8000/docs
```

FastAPI automatically provides Swagger UI for testing your APIs.

---

# Available Endpoints

| Method | Endpoint | Description |
|--------|----------|------------|
| POST   | /users/ | Create user |
| GET    | /users/ | Get all users |
| GET    | /users/{id} | Get single user |
| PUT    | /users/{id} | Update user |
| DELETE | /users/{id} | Delete user |

---

# 🚀 Project Architecture

Frontend → FastAPI → SQLAlchemy → SQLite Database

---

# ⚠️ Assis. Notes

- Replace `allow_origins=["*"]` with frontend URL
- Use PostgreSQL  or any other DB instead of SQLite
- Add authentication (JWT)
- Use dependency injection properly (`Depends(get_db)`)
- Add migrations (Alembic)

---
