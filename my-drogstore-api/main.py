from fastapi import FastAPI, Body, Query, Request, HTTPException,Depends
from fastapi.responses import HTMLResponse
#Devolver respuesta en formato json
from fastapi.responses import JSONResponse 

#forma de envio de parametros
from pydantic import BaseModel
from typing import Optional

#devolvera una lista y esta lo definimos en la funcion de esta form (-> List[])
from typing import List

# Para validar campos
from pydantic import  Field

from fastapi.security import HTTPBearer
from starlette.requests import Request

from jwt_manager import create_token, validate_token
 
app = FastAPI()
app.title ="Api de Farmacia"
app.version = "0.0.1"


list_farmacia =[
    {
         "id": 1,
        "producto": "panadol",
        "precio": 2,
        "descripcion": "para el dolor",
        "tipo": "aines",
    },
        {
         "id": 2,
        "producto": "clorfenamina",
        "precio": 4,
        "descripcion": "para el resfrio",
        "tipo": "no aines",
    },
        {
         "id": 3,
        "producto": "algodon",
        "precio": 10,
        "descripcion": "para primeros auxilios",
        "tipo": "libre",
    }
    ]

class Farmacia(BaseModel):
     id: Optional[int] = None
     producto: str = Field( max_length=15)
     precio: int 
     descripcion: str = Field( max_length=50)
     tipo: str = Field( max_length=50)

     class Config:
          schema_extra = {
               "example" : {
                    "id": 1,
                    "producto": "panadol",
                    "precio": 2,
                    "descripcion": "para el dolor",
                    "tipo": "aines", 
               }
          }

class User(BaseModel):
     email: str
     password: str

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
         auth = await super().__call__(request)
         data = validate_token(auth.credentials)
         if data["email"] != "drogstore@gmail.com":
              raise HTTPException(status_code=403, detail="Credenciales inválidas")


@app.post("/login", tags=["Auth"])
def login(User: User):
     if (User.email=="drogstore@gmail.com" and User.password =="@auth@1988@"):
         token: str = create_token(User.dict())
         return JSONResponse(content=token)





@app.get("/saludo", tags=["Saludos"])
def Saludar():
    return "Saludos a todos"



@app.get("/pagina", tags=["Saludos"])
def pagina():
    return HTMLResponse("<h1> Farmacia Global </h1>")


@app.get("/obtener_listado", tags=["Funciones"], response_model=List[Farmacia], dependencies=[Depends(JWTBearer())] )
def get_Farmacia() -> List[Farmacia]:
    return list_farmacia


@app.get("/obtener_medicamento_by_id/{id}", tags=["Funciones"], response_model=Farmacia)
def get_medicamento(id: int) ->  Farmacia : 
    medicamento = list(filter(lambda item: item["id"] == id, list_farmacia))
    #como estoy obteniendo la lista con todo y [],voy a sacar el resultado 
    medicamento = medicamento[0]
    return JSONResponse(content=medicamento)

@app.post("/registrar_medicamento", tags=["Funciones"], response_model=dict)
def registrar_medicamento(id: int = Body(), producto: str = Body(), precio: int = Body(), descripcion: str = Body(), tipo: str = Body()):
     list_farmacia.append(
             {
                "id"  : id,
                "producto": producto,
                "precio": precio,
                "descripcion": descripcion,
                "tipo": tipo,
             }
        )
     return JSONResponse(content={"message": "Se registró el medicamento"})

@app.post("/registrar_medicamento_basemodel", tags=["Funciones"], response_model= dict)
def registrar_medicamento_BaseModel(farmacia: Farmacia) -> dict:
    list_farmacia.append(farmacia.dict())
    return JSONResponse(content={"message": "Se registró el medicamento"})


@app.put("/modificar_medicamento/{id}", tags=["Funciones"], response_model=dict)
def put_medicamento(id: int , producto: str = Body(), precio: int = Body(), descripcion: str = Body(), tipo: str = Body()) -> dict:
    for item in list_farmacia:
          if item["id"] == id:
               item["producto"] = producto
               item["precio"] = precio
               item["descripcion"] =descripcion
               item["tipo"] =tipo
    
    return JSONResponse(content={"message": "Se modificó el medicamento"})

@app.put("/modificar_medicamento_basemodel/{id}", tags=["Funciones"], response_model=dict)
def put_medicamento_basemodel(id: int , farmacia: Farmacia) -> dict:
    print("holaaaa")
    for item in list_farmacia:
          if item["id"] == id:
               item["producto"] = farmacia.producto
               item["precio"] = farmacia.precio
               item["descripcion"] = farmacia.descripcion
               item["tipo"] = farmacia.tipo
               print("datos")
          print("datos--")
    return JSONResponse(content={"message": "Se modificó el medicamento"})


@app.delete("/eliminar_medicamento/{id}", tags=["Funciones"], response_model=dict)
def delete_medicamento(id: int) -> dict:
    for item in list_farmacia:
         if item["id"] == id:
              list_farmacia.remove(item)
    
    return JSONResponse(content={"message": "Se eliminó el medicamento"})



#TIPO QUERY
@app.get("/obtener_medicamento_by_tipo/", tags=["Funciones Query"], response_model= List[Farmacia])
def Get_medicamento_tipo_by_tipo(tipo: str = Query(min_length=5, max_length=15)) -> List[Farmacia]:
      data = list(filter(lambda item: item["tipo"] == tipo, list_farmacia))
      return JSONResponse(content=data)


@app.post("/registrar_medicamento_query", tags=["Funciones Query"], response_model=dict)
def Registrar_medicamento_QUERY(id: int, producto: str, precio: int, descripcion: str, tipo: str) -> dict:
        list_farmacia.append(
             {
                "id"  : id,
                "producto": producto,
                "precio": precio,
                "descripcion": descripcion,
                "tipo": tipo,
             }
        )
        return JSONResponse(content={"message": "Se registró el medicamento"})

