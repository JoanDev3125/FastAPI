from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security.http import HTTPAuthorizationCredentials
from pydantic import BaseModel
from pydantic import Field
from typing import Optional, List

from starlette.requests import Request
from jwt_manager import create_token, validate_token
from fastapi.security import HTTPBearer

app = FastAPI()
app.title = "Ferreteria"
app.version = "0.0.1"


ferreteria_prod = [
    {
        "id": 1,
        "producto": "Martillo",
        "precio": 115,
        "descripcion": "lorem....",
        "tipo": "construcción",
    },
    {
        "id": 2,
        "producto": "Sprite",
        "precio": 9,
        "descripcion": "lorem....",
        "tipo": "pintura",
    },
    {
        "id": 3,
        "producto": "tubo 4",
        "precio": 32,
        "descripcion": "lorem....",
        "tipo": "plomeria",
    },
]


class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data["email"] != "ferreteria@gmail.com":
            raise HTTPException(status_code=403, detail="credenciales inválidas")


class User(BaseModel):
    email: str
    password: str


class Ferreteria(BaseModel):
    id: Optional[int] = None
    producto: str = Field(min_length=5, max_length=15)
    precio: int
    descripcion: str
    tipo: str

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "producto": "Martillo",
                "precio": 15,
                "descripcion": "lorem....",
                "tipo": "construcción",
            }
        }


@app.get("/saludar", tags={"Home"})
def saludar():
    return "Saludos para todos"


@app.get("/mensaje", tags={"Home"})
def mensaje():
    return HTMLResponse("<h1>mensaje</h1>")


@app.post("/login", tags=["auth"])
def login(user: User):
    if user.email == "ferreteria@gmail.com" and user.password == "@ferreteria1988@":
        token: str = create_token(user.dict())
        return JSONResponse(content=token)


@app.get("/listar", tags={"Ferreteria"}, response_model=List[Ferreteria])
def listado() -> List[Ferreteria]:
    # return ferreteria_prod
    return JSONResponse(content=ferreteria_prod)


@app.get(
    "/listar_by_id/{id}",
    tags={"Ferreteria"},
    response_model=Ferreteria,
    status_code=200,
    dependencies=[Depends(JWTBearer())],
)
def listado_id(id: int) -> Ferreteria:
    # return list(filter(lambda item: item["id"] == id, ferreteria_prod))
    listado_filtrado = list(filter(lambda item: item["id"] == id, ferreteria_prod))
    return JSONResponse(status_code=200, content=listado_filtrado[0])


@app.post("/agregar", tags={"Ferreteria"}, response_model=dict, status_code=201)
def agregar_listado(ferreteria: Ferreteria) -> dict:
    ferreteria_prod.append(ferreteria.dict())
    return JSONResponse(
        status_code=201, content={"message": "Se registró el producto con éxito"}
    )


@app.put("/actualizar/{id}", tags={"Ferreteria"}, response_model=dict)
def actualizar_listado(id: int, ferreteria: Ferreteria) -> dict:
    for item in ferreteria_prod:
        if item["id"] == id:
            item["producto"] = ferreteria.producto
            item["precio"] = ferreteria.precio
            item["descripcion"] = ferreteria.descripcion
            item["tipo"] = ferreteria.tipo
    return JSONResponse(content={"message": "Se ha modificado el producto"})


@app.delete("/eliminar/{id}", tags={"Ferreteria"}, response_model=dict)
def eliminar_producto(id: int) -> dict:
    for item in ferreteria_prod:
        if item["id"] == id:
            ferreteria_prod.remove(item)

    return JSONResponse(content={"message": "Se ha eliminado el producto"})
