import uvicorn
from fastapi import FastAPI, Query

app = FastAPI()


hotels = [
    {"id": 1, "title": 'Sochi'},
    {"id": 2, "title": "Dubai"}
]


@app.get("/hotels")
def get_hotels(
        id: int | None = Query(None, description='Айдишник'),
        title: str | None = Query(None, description='Название отеля'),
):
    _hotels = []
    for hotel in hotels:
        if id and id != hotel["id"]:
            continue
        if title and title != hotel["title"]:
            continue
        _hotels.append(hotel)
    return _hotels


if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", reload=True)
