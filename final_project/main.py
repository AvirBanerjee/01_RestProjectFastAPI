from fastapi import FastApi,HTTPException
from fastapi.middleware.cors import CORSMiddleware

from fastapi.security import OAuth2PasswordBearer ,OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import List
from sqlalchemy import create_engine,Column,Integer,String
from sqlalchemy.orm import declarative_base ,sessionmaker,Session

from jose import jwt,JWTError
from passlib.context import CryptContext
from datetime import datetime,timedelta
