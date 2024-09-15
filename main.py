import uvicorn
from fastapi import FastAPI, Query, Body

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


@app.post("/hotels")
def create_hotel(
        title: str = Body(embed=True),
):
    global hotels
    hotels.append({
        "id": hotels[-1]['id'] + 1,
        'title': title
    })
    return {"status": "OK"}


@app.delete("/hotels/{hotel_id}")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel_id != hotel["id"]]
    return {"status": "OK"}


if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", reload=True)
