import uvicorn
from fastapi import FastAPI, Query, Body

app = FastAPI()


hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Dubai", "name": "dubai"}
]


@app.get("/hotels")
def get_hotels(
        id: int | None = Query(None, description='Айдишник'),
        title: str | None = Query(None, description='Название отеля'),
        name: str | None = Query(None, description='Название отеля 2'),
):
    _hotels = []
    for hotel in hotels:
        if id and id != hotel["id"]:
            continue
        if title and title != hotel["title"]:
            continue
        if name and name != hotel["name"]:
            continue
        _hotels.append(hotel)
    return _hotels


@app.post("/hotels")
def create_hotel(
        title: str = Body(embed=True),
        name: str = Body(embed=True),
):
    global hotels
    hotels.append({
        "id": hotels[-1]['id'] + 1,
        "title": title,
        "name": name,
    })
    return {"status": "OK"}


@app.put("/hotels/{hotel_id}")
def put_hotel(
        hotel_id: int,
        title: str = Body(),
        name: str = Body(),
):
    for hotel in hotels:
        if hotel_id == hotel["id"]:
            hotel["title"] = title
            hotel["name"] = name
            return {"status": "OK"}
    return {"status": "Not found"}


@app.patch(
    "/hotels/{hotel_id}",
    summary='Частичное обновление данных об отеле',
    description='<h1>Частично обновляем данные об отеле: можно отправить name, а можно title</h1>',
)
def patch_hotel(
        hotel_id: int,
        title: str | None = Body(None),
        name: str | None = Body(None),
):
    for hotel in hotels:
        if hotel_id == hotel["id"]:
            hotel["title"] = title if title else hotel["title"]
            hotel["name"] = name if name else hotel["name"]
            return {"status": "OK"}
    return {"status": "Not found"}


@app.delete("/hotels/{hotel_id}")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel_id != hotel["id"]]
    return {"status": "OK"}


if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", reload=True)
