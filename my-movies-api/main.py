from fastapi import Depends, FastAPI, Body, Path, Query, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse


# from pydantic import BaseModel, Field
from pydantic import BaseModel
from pydantic import Field
from typing import Optional

from starlette.requests import Request
from jwt_manager import create_token, validate_token
from fastapi.security import HTTPBearer


app = FastAPI()
app.title = "Mi nueva aplicación con FastApi"
app.version = "0.0.1"


class JWTBeaver(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data["email"] != "jparedesy@gmail.com":
            raise HTTPException(status_code=403, detail="Credenciales inválidas")


class User(BaseModel):
    email: str
    password: str


class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(max_length=17)
    overview: str
    year: int
    rating: float
    category: str

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "title": "Mi pelicula",
                "overview": "descripción",
                "year": 2022,
                "rating": 5.5,
                "category": "Acción",
            }
        }


movies = [
    {
        "id": 1,
        "title": "Avatar",
        "overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        "year": "2009",
        "rating": 7.8,
        "category": "Acción",
    },
    {
        "id": 2,
        "title": "Stranger Thinks",
        "overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        "year": "2016",
        "rating": 7.8,
        "category": "Terror",
    },
]


@app.get("/saludos", tags=["home"])
def message():
    return "Hello world!"


@app.post("/login", tags=["auth"])
def login(user: User):
    if user.email == "jparedesy@gmail.com" and user.password == "admin":
        token: str = create_token(user.dict())
        return JSONResponse(content=token)


@app.get("/pagina", tags=["home"])
def pagina():
    return HTMLResponse("<h1>Mi primer titulo</h1>")


@app.get(
    "/movies", tags=["movies"], dependencies=[Depends(JWTBeaver())], status_code=200
)
def get_movies():
    # return movies
    return JSONResponse(status_code=200, content=movies)


@app.get("/movies/{id}", tags=["movies"], dependencies=[Depends(JWTBeaver())])
def get_movie_id(id: int = Path(ge=1, le=2000)):
    return JSONResponse(content=list(filter(lambda item: item["id"] == id, movies)))


@app.get("/movies_params", tags=["movies"])
def get_movies_param(
    category: str = Query(min_length=5, max_length=15), year: int = Query(ge=1)
):
    return JSONResponse(
        content=list(
            filter(
                lambda item: item["category"] == category and int(item["year"]) == year,
                movies,
            )
        )
    )


@app.post("/movies_post", tags=["movies"])
def create_movie(
    id: int = Body(),
    title: str = Body(),
    overview: str = Body(),
    year: int = Body(),
    rating: float = Body(),
    category: str = Body(),
):
    movies.append(
        {
            "id": id,
            "title": title,
            "overview": overview,
            "year": year,
            "rating": rating,
            "category": category,
        }
    )
    # return movies
    return JSONResponse(content={"message": "Se realizó el registro de la película"})


@app.post("/movies_post_schema", tags=["movies"])
def create_movie_schema(movie: Movie):
    movies.append(movie.dict())
    # return movies
    return JSONResponse(content={"message": "Se realizó el registro de la película"})


@app.put("/actualizar_movies/{id}", tags={"movies"})
def update_movies(
    id: int,
    title: str = Body(),
    overview: str = Body(),
    year: int = Body(),
    rating: float = Body(),
    category: str = Body(),
):
    for item in movies:
        if item["id"] == id:
            item["title"] = title
            item["overview"] = overview
            item["year"] = year
            item["rating"] = rating
            item["category"] = category

    # return movies
    return JSONResponse(
        content={"message": "Se realizó la modificación de la película"}
    )


@app.put("/actualizar_movies_schema/{id}", tags={"movies"})
def update_movies_schema(id: int, pelicula: Movie):
    for item in movies:
        if item["id"] == id:
            item["title"] = pelicula.title
            item["overview"] = pelicula.overview
            item["year"] = pelicula.year
            item["rating"] = pelicula.rating
            item["category"] = pelicula.category

    # return movies
    return JSONResponse(
        content={"message": "Se realizó la modificación de la película"}
    )


@app.delete("/eliminar_movies/{id}", tags={"movies"})
def delete_movie(id: int):
    for item in movies:
        if item["id"] == id:
            movies.remove(item)
    # return movies
    return JSONResponse(content={"message": "Se realizó la eliminación de la película"})
