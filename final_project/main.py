from fastapi import FastAPI,HTTPException,Depends
from fastapi.middleware.cors import CORSMiddleware

from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import List
from sqlalchemy import create_engine,Column,Integer,String,Boolean,ForeignKey
from sqlalchemy.orm import declarative_base ,sessionmaker,Session,relationship

from jose import jwt,JWTError
from passlib.context import CryptContext
from datetime import datetime,timedelta

#APP
app=FastAPI(
    title="Employee Managment Api",
    version="1.0"
)

#CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],#Needs to be changed in future #typo in allow_orgins
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
    email=Column(String,unique=True)
    password=Column(String)

    employs=relationship("EmployDB",back_populates="owner") # back_populates typo error

class EmployDB(Base):
    __tablename__="employs"

    id=Column(Integer,primary_key=True,index=True)
    fullname=Column(String)
    email=Column(String,unique=True) #unique typo error
    isOnProject=Column(Boolean)
    experience=Column(Integer)
    completed=Column(Integer)
    description=Column(String)

    user_id = Column(Integer, ForeignKey("users.id")) # changed
    owner=relationship("UserDB",back_populates="employs")

Base.metadata.create_all(bind=engine)

# schemas
class UserCreate(BaseModel):
    id:int
    fullname: str
    email: str
    password: str # password added

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
    access_token:str # changed = with :
    token_type:str

# security 

SECRET_KEY="SUPERSECRETSHHHHHHHHH"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=60

pwd_context=CryptContext(
    schemes=["bcrypt"], #typo of bcryt
    deprecated="auto"
)

def hash_password(password:str) ->str:
    return pwd_context.hash(password)

oauth2_scheme=OAuth2PasswordBearer(
    tokenUrl="/api/v1/login"
)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()    

def verify_password(plain,hashed):
    return pwd_context.verify(plain,hashed)
   
def create_access_token(data:dict):
    to_encode=data.copy()
    expire=datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    token=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return token

def get_current_user(
        token:str =Depends(oauth2_scheme),
        db: Session =Depends(get_db)
    ):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        email = payload.get("email")
        if email is None:
            raise HTTPException(status_code=401,detail="Invalid Token")
    except JWTError:
        raise HTTPException(status_code=401,detail="Token error")   
    user=db.query(UserDB).filter(UserDB.email == email).first()
    if user is None:
        raise HTTPException(status_code=401,detail="User not found")
    return user

API_V1="/api/v1"

#register
@app.post(API_V1 + "/register",response_model=UserResponse)
def register_user(user:UserCreate,db:Session=Depends(get_db)):
    existing=db.query(UserDB).filter(UserDB.email==user.email).first()
    if existing:
        raise HTTPException(status_code=400,detail="User already exixts")
    new_user=UserDB(
        fullname=user.fullname,
        email=user.email,
        password=hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

#login
@app.post(API_V1 + "/login",response_model=Token)
def login_user(
    form_data:OAuth2PasswordRequestForm=Depends(),
    db:Session = Depends(get_db)
    ):
    user=db.query(UserDB).filter(UserDB.email == form_data.username).first()
    if not user:
        raise HTTPException(status_code=400,detail="Invalid Email")
    if not verify_password(form_data.password,user.password):
        raise HTTPException(status_code=400,detail="Invalid password")  
    access_token=create_access_token(
        data={"email":user.email}
    )    
    return{
        "access_token":access_token,
        "token_type":"bearer"
    }

@app.get(API_V1 + "/dashboard")
def dashboard(current_user:UserDB=Depends(get_current_user)):
    return{
        "fullname":current_user.fullname,
        "email":current_user.email,
        "total_employs":len(current_user.employs)
    }

#creating employee
@app.post(API_V1+"/employ")
def create_employ(
    employ:EmployCreate,
    db: Session =Depends(get_db),
    current_user:UserDB =Depends(get_current_user)
    ):
    new_employ=EmployDB(
        fullname=employ.fullname,
        email=employ.email,
        isOnProject=employ.isOnProject,
        experience=employ.experience,
        completed=employ.completed,
        description=employ.description,
        owner=current_user
    )
    db.add(new_employ)
    db.commit()

    return{
        "message":"employ created succesfully"
        }

# get all users
@app.get(API_V1 + "/employs")
def get_employs(
    db: Session = Depends(get_db),
    current_user:UserDB = Depends(get_current_user)
    ):
    return current_user.employs

# get single user
@app.get(API_V1 + "/employ/{id}")
def get_employ(
    id:int,
    db: Session = Depends(get_db),
    current_user:UserDB = Depends(get_current_user)
    ):
    employ=db.query(EmployDB).filter(EmployDB.id == id).first()
    if not employ:
        raise HTTPException(status_code=404,detail="Employee not found")
    return employ

# update employe
@app.put(API_V1 +"/employ/{id}")
def update_employ(
    id:int,
    data:EmployCreate,
    db: Session = Depends(get_db),
    current_user:UserDB = Depends(get_current_user)
    ):
    employ=db.query(EmployDB).filter(EmployDB.id == id).first()
    if not employ:
        raise HTTPException(status_code=404,detail="Employee not found")
    #removed commas bcoz it was making it tupple insted of assignment
    employ.fullname=data.fullname
    employ.email=data.email
    employ.isOnProject=data.isOnProject
    employ.experience=data.experience
    employ.completed=data.completed
    employ.description=data.description
    
    db.commit()
    return { "message":"employee updated successfully"}

# Delete employee
@app.delete(API_V1 + "/employ/{id}")
def delete_employ( # name change from get_employ
    id:int,
    db: Session = Depends(get_db),
    current_user:UserDB = Depends(get_current_user)
    ):
    employ=db.query(EmployDB).filter(EmployDB.id == id).first()
    if not employ:
        raise HTTPException(status_code=404,detail="Employee not found")
    db.delete(employ)
    db.commit()

    return {"message":"Employee deleted succesfull"}