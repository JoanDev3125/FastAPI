from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()
app.title = "Mi nueva aplicación con FastApi"
app.version = "0.0.1"


class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(max_length=15)
    overview: str
    year: int
    rating: float
    category: str


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


@app.get("/pagina", tags=["home"])
def pagina():
    return HTMLResponse("<h1>Mi primer titulo</h1>")


@app.get("/movies", tags=["movies"])
def get_movies():
    return movies


@app.get("/movies/{id}", tags=["movies"])
def get_movie_id(id: int):
    return list(filter(lambda item: item["id"] == id, movies))


@app.get("/movies_params", tags=["movies"])
def get_movies_param(category: str, year: int):
    return list(
        filter(
            lambda item: item["category"] == category and int(item["year"]) == year,
            movies,
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
    return movies


@app.post("/movies_post_schema", tags=["movies"])
def create_movie_schema(movie: Movie):
    movies.append(movie.dict())
    return movies


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

    return movies


@app.put("/actualizar_movies_schema/{id}", tags={"movies"})
def update_movies_schema(id: int, pelicula: Movie):
    for item in movies:
        if item["id"] == id:
            item["title"] = pelicula.title
            item["overview"] = pelicula.overview
            item["year"] = pelicula.year
            item["rating"] = pelicula.rating
            item["category"] = pelicula.category

    return movies


@app.delete("/eliminar_movies/{id}", tags={"movies"})
def delete_movie(id: int):
    for item in movies:
        if item["id"] == id:
            movies.remove(item)
    return movies
