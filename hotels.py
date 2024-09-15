from fastapi import Query, APIRouter, Body

from shemas.hotels import Hotel, HotelPATCH

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
def create_hotel(hotel_data: Hotel = Body(openapi_examples={
    "1": {
        "summary": "Сочи",
        "value": {
            "title": "Отель Сочи 5 stars",
            "name": "sochi_5",
        }
    },
    "2": {
        "summary": "Дубай",
        "value": {
            "title": "Отель дубай back one",
            "name": "dubai back one",
        },
    },
})):
    global hotels
    hotels.append({
        "id": hotels[-1]['id'] + 1,
        "title": hotel_data.title,
        "name": hotel_data.name,
    })
    return {"status": "OK"}


@router.put("/{hotel_id}", summary='Изменение данных об отеле')
def put_hotel(hotel_id: int, hotel_data: Hotel):
    for hotel in hotels:
        if hotel_id == hotel["id"]:
            hotel["title"] = hotel_data.title
            hotel["name"] = hotel_data.name
            return {"status": "OK"}
    return {"status": "Not found"}


@router.patch(
    "/{hotel_id}",
    summary='Частичное обновление данных об отеле',
    description='<h1>Частично обновляем данные об отеле: можно отправить name, а можно title</h1>',
)
def patch_hotel(hotel_id: int, hotel_data: HotelPATCH):
    for hotel in hotels:
        if hotel_id == hotel["id"]:
            hotel["title"] = hotel_data.title if hotel_data.title else hotel["title"]
            hotel["name"] = hotel_data.name if hotel_data.name else hotel["name"]
            return {"status": "OK"}
    return {"status": "Not found"}


@router.delete("/{hotel_id}", summary='Удаление отеля')
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel_id != hotel["id"]]
    return {"status": "OK"}
