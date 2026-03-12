from fastapi import FastAPI , HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from sqlalchemy import create_engine, Column ,Integer,String
from sqlalchemy.orm import declarative_base , sessionmaker , Session

#DB 

DATABASE_URL="sqlite:///./test.db"
engine=create_engine(
    DATABASE_URL , connect_args={"check_same_thread":False}
)

SessionLocal=sessionmaker(bind=engine,autoflush=False,autocommit=False)

Base=declarative_base()

# DB MOdel

class UserDB(Base):
    __tablename__="users"

    id=Column(Integer,primary_key=True,index=True)
    name=Column(String)
    email=Column(String)

Base.metadata.create_all(bind=engine)

#schema
class UserCreate(BaseModel):
    name:str
    email:str

class UserResponse(BaseModel):
    id:int
    name:str
    email:str

    class Config:
        from_attributes=True


app=FastAPI()

# cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close

#Create
@app.post("/users",response_model=UserResponse)
def create_user(user:UserCreate):
    db:Session = SessionLocal()

    db_user = UserDB(name=user.name,email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    db.close()# upadted db.close

    return db_user

#Read
@app.get("/users/", response_model=List[UserResponse])
def get_users():
    db: Session = SessionLocal()
    users = db.query(UserDB).all()
    db.close()
    return users

# read user->1
@app.get("/users/{user_id}",response_model= UserResponse)
def get_user(user_id:int):
    db: Session = SessionLocal()
    user=db.query(UserDB).filter(UserDB.id==user_id).first()
    db.close()
    if not user:
        raise HTTPException(status_code=404,detail="User not found")
    return user    

#Update
@app.put("/users/{user_id}",response_model=UserResponse)
def update_user(user_id:int,updated_user:UserCreate):
    db:Session=SessionLocal()
    user=db.query(UserDB).filter(UserDB.id==user_id).first()
    if not user:
        db.close()
        raise HTTPException(status_code=404,detail="User not found")
    user.name=updated_user.name
    user.email=updated_user.email

    db.commit()
    db.refresh(user)
    db.close()

    return user

#delete

@app.delete("/users/{user_id}")
def delete_user(user_id:int):
    db:Session=SessionLocal()
    user=db.query(UserDB).filter(UserDB.id==user_id).first()
    if not user:
        db.close()
        raise HTTPException(status_code=404,detail="User not found")
    db.delete(user)
    db.commit()
    db.close()
    return {"message":"USer deleted successfully"}