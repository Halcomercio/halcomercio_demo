from fastapi import FastAPI, HTTPException, status, Depends
from fastapi import UploadFile, File
from fastapi.security import HTTPBasic
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from urllib import response
from typing import List
from pydantic import BaseModel
from os import stat
import sqlite3
import requests
import pyrebase
import os
from os import listdir, getcwd
from IPython.core.display import Image

app = FastAPI()

security = HTTPBasic()

DATABASE_URL = os.path.join("backend/productos.sqlite")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Firebase Config
firebaseConfig = {
    "apiKey": "AIzaSyC3PoYDiqlXZrPVUVZoXwxkVytty6vGugQ",
    "authDomain": "halcomercio.firebaseapp.com",
    "databaseURL": "https://halcomercio-default-rtdb.firebaseio.com",
    "projectId": "halcomercio",
    "storageBucket": "halcomercio.appspot.com",
    "messagingSenderId": "268615225240",
    "appId": "1:268615225240:web:3a5fd0040d0211ea3e25ed",
    "measurementId": "G-V6906MN0GJ",
}

firebase = pyrebase.initialize_app(firebaseConfig)
storage = firebase.storage()
# Models


class Response(BaseModel):
    status: str
    message: str


class User_Login(BaseModel):
    email: str
    password: str


class User_Register(BaseModel):
    name: str
    matricula: str
    email: str
    password: str
    carrera: str
    telefono: str


class Producto(BaseModel):
    nombre: str
    descripcion: str
    precio: float
    categoria: str
    stock: int
    uid_vendedor: str


class ResetPassword(BaseModel):
    email: str


# Routes


@app.get("/", response_model=Response)
async def index():
    return Response(status="success", message="Welcome to the API")


@app.post(
    "/register",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Register a new user",
    description="Register a new user",
    tags=["User"],
)
async def register(user: User_Register):
    auth = firebase.auth()
    db = firebase.database()
    email = user.email
    password = user.password
    name = user.name
    matricula = user.matricula
    telefono = user.telefono
    carrera = user.carrera

    try:
        user_info = auth.create_user_with_email_and_password(email, password)
        idTokenU = user_info["idToken"]
        user = auth.get_account_info(idTokenU)
        emailV = auth.send_email_verification(idTokenU)
        uid = user["users"][0]["localId"]
        data = {
            "Nombre": name,
            "Matricula": matricula,
            "Email": email,
            "Carrera": carrera,
            "Telefono": telefono,
        }
        result = db.child("users").child(uid).set(data)
        response = {"user_info": user_info}
        return response

    except Exception as error:
        print(f"Error : {error}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Error")


@app.post(
    "/signin",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Sign in a user",
    description="Sign in a user",
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
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Error")


@app.post(
    "/passwordR",
    summary="Recover Password",
    description="Recover Password",
    tags=["User"],
)
async def resetPassword(user: ResetPassword):
    auth = firebase.auth()
    email = user.email
    auth.send_password_reset_email(email)


@app.post("/uploadImage")
async def createFile(files: UploadFile = File(...)):
    pwd_clod = "producto/" + files.filename
    up = storage.child(pwd_clod).put(files.file)
    return pwd_clod


@app.get("/downloadImage/{file_name}")
async def downloadImage(file_name: str):
    url = storage.child(file_name).get_url(None)
    return url


@app.get("/getProducts", status_code=status.HTTP_200_OK)
async def getProducts():
    with sqlite3.connect("backend/productos.sqlite") as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute(
            "SELECT nombre,descripcion,precio,stock,categoria FROM productoss"
        )
        productos = cursor.fetchall()
    return productos


@app.post("/addProduct", status_code=status.HTTP_200_OK)
async def addProduct(productos: Producto):
    with sqlite3.connect("backend/productos.sqlite") as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO productoss('nombre','descripcion','precio','stock','categoria','uid_vendedor') VALUES(?,?,?,?,?,?)",
            (
                productos.nombre,
                productos.descripcion,
                productos.precio,
                productos.stock,
                productos.categoria,
                productos.uid_vendedor,
            ),
        )
        connection.commit()
    return {"status": "success"}


@app.post("/imagedb")
async def imagedb(files: UploadFile):
    ext = os.path.splitext(files.filename)
    if files.content_type not in ["image/png", "image/jpeg"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid image"
        )
    path_image = "images/" + files.filename
    with sqlite3.connect("backend/productos.sqlite") as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute("INSERT INTO imagenes(img) VALUES ('{}')".format(path_image))
        connection.commit()
    return Response(status="success", message="Imagen Agregada")
