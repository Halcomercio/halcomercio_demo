from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import RedirectResponse
from urllib import response
from typing import List
from pydantic import BaseModel
from os import stat
import sqlite3
import requests
import pyrebase


app = FastAPI()

security = HTTPBasic()

# Firebase Config
firebaseConfig = {
  "apiKey": "AIzaSyC3PoYDiqlXZrPVUVZoXwxkVytty6vGugQ",
  "authDomain": "halcomercio.firebaseapp.com",
  "databaseURL": "https://halcomercio-default-rtdb.firebaseio.com",
  "projectId": "halcomercio",
  "storageBucket": "halcomercio.appspot.com",
  "messagingSenderId": "268615225240",
  "appId": "1:268615225240:web:3a5fd0040d0211ea3e25ed",
  "measurementId": "G-V6906MN0GJ"
}

firebase = pyrebase.initialize_app(firebaseConfig)

# Models

class Response(BaseModel):
    status: str
    message: str
class User_Login(BaseModel):
    email: str
    password: str

class User_Register(BaseModel):
    name: str
    matricula : str
    email: str
    password: str

class Producto(BaseModel):
    name: str
    price : str
    category : str
    major : str
    
# Routes

@app.get("/", response_model=Response)
async def index():
    return Response(status="success", message="Welcome to the API")

@app.post(
    "/register",
    status_code=status.HTTP_202_ACCEPTED,
    summary = "Register a new user",
    description = "Register a new user",
    tags=["User"],
)
async def register(user: User_Register):
    auth = firebase.auth()
    db = firebase.database()
    email = user.email
    password = user.password
    name = user.name
    matricula = user.matricula  
    
    try:
        user_info = auth.create_user_with_email_and_password(email, password)
        
        idToken = user_info["idToken"]
        user = auth.get_account_info(idToken)
               
        return user
    
    except Exception as error:
        print(f"Error : {error}")
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Error")

@app.post(
    "/signin",  
    status_code=status.HTTP_202_ACCEPTED,
    summary = "Sign in a user",
    description = "Sign in a user",
    tags=["User"],
)
async def signin(user: User_Login):
    auth = firebase.auth()
    email = user.email
    password = user.password
    
    try:
        user_info = auth.sign_in_with_email_and_password(email, password)
        idToken = user_info["idToken"]
        return idToken
    except Exception as error:
        print(f"Error : {error}")
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Error")

