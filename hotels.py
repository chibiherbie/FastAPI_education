from fastapi import Query, Body, APIRouter

router = APIRouter(prefix='/hotels', tags=['Отели'])

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Dubai", "name": "dubai"}
]


@router.get("/", summary='Получение отелей')
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


@router.post("/", summary='Добавление нового отеля')
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


@router.put("/{hotel_id}", summary='Изменение данных об отеле')
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


@router.patch(
    "/{hotel_id}",
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


@router.delete("/{hotel_id}", summary='Удаление отеля')
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel_id != hotel["id"]]
    return {"status": "OK"}
