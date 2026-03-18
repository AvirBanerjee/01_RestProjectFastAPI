from fastapi import FastApi,HTTPException
from fastapi.middleware.cors import CORSMiddleware

from fastapi.security import OAuth2PasswordBearer ,OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import List
from sqlalchemy import create_engine,Column,Integer,String,Boolean,Foreignkey
from sqlalchemy.orm import declarative_base ,sessionmaker,Session,relationship

from jose import jwt,JWTError
from passlib.context import CryptContext
from datetime import datetime,timedelta

#APP
app=FastApi(
    title="Employee Managment Api",
    version="1.0"
)

#CORS
app.add_middleware(
    CORSMiddleware,
    allow_orgins=["*"],#Needs to be changed in future
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

#DB
DATABASE_URL="sqlite:///./app.db"

engine=create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread":False}
)

SessionLocal=sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base=declarative_base()

# Models

class UserDB(Base):
    __tablename__="users"

    id=Column(Integer,primary_key=True,index=True)
    fullname=Column(String)
    email=Column(String,unqiue=True)
    password=Column(String)

    employs=relationship("EmployDB",back_populated="owner")

class EmployDB(Base):
    __tablename__="employs"

    id=Column(Integer,primary_key=True,index=True)
    fullname=Column(String)
    email=Column(String,unqiue=True)
    isOnProject=Column(Boolean)
    experience=Column(Integer)
    completed=Column(Integer)
    description=Column(String)

    user_id=Column(Integer,Foreignkey("user_id"))
    owner=relationship("UserDB",back_populates="employs")

Base.metadata.create_all(bind=engine)

# schemas
class UserCreate(BaseModel):
    id:int
    fullname:str
    email:str

    class Config:
        orm_mode=True
class UserResponse(BaseModel):
    id:int
    fullname:str
    email:str

    class Config:
        orm_mode=True

class EmployCreate(BaseModel):
    fullname:str
    email:str
    isOnProject:bool
    experience:int
    completed:int
    description:str

class Token(BaseModel):
    access_token=str
    token_type:str

