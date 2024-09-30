from datetime import date

from fastapi import Query, APIRouter, Body, HTTPException
from sqlalchemy.exc import MultipleResultsFound

from src.api.dependecies import DBDep
from src.shemas.rooms import Room, RoomPatch, RoomAdd, RoomAddRequest, RoomPatchRequest

DEFAULT_PER_PAGE = 3

router = APIRouter(prefix='/hotels', tags=['Номера'])


@router.get("/{hotel_id}/rooms", summary='Получение номера')
async def get_rooms(
        db: DBDep,
        hotel_id: int,
        date_from: date = Query(example="2024-10-02"),
        date_to: date = Query(example="2024-10-08"),
):
    return await db.rooms.get_filtered_by_time(hotel_id=hotel_id, date_from=date_from, date_to=date_to)


@router.get("/{hotel_id}/rooms/{room_id}", summary='Получение номера в отеле по id')
async def get_room(hotel_id: int, room_id: int, db: DBDep):
    return await db.rooms.get_one_or_none(hotel_id=hotel_id, id=room_id)


@router.post("/{hotel_id}/rooms/", summary='Добавление нового номера')
async def create_room(
        hotel_id: int,
        db: DBDep,
        room_data: RoomAddRequest = Body(openapi_examples={
            "1": {
                "summary": "Базовая комната",
                "value": {
                    "title": "Базовая комната",
                    "price": 1000,
                    "quantity": 2,
                }
            },
            "2": {
                "summary": "Премиум комната",
                "value": {
                    "title": "Премиум комната",
                    "price": 3000,
                    "quantity": 2,
                    "description": "Премиум комната со всеми удобствами для всей семьи",
                }
            },
        })
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    room = await db.rooms.add(_room_data)
    await db.commit()

    return {"status": "OK", "data": room}


@router.put("/{hotel_id}/rooms/{room_id}", summary='Изменение данных в номере')
async def put_room(hotel_id: int, room_id: int, room_data: RoomAddRequest, db: DBDep):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    try:
        hotel = await db.rooms.edit(_room_data, id=room_id)
        await db.commit()
    except MultipleResultsFound as e:
        return HTTPException(status_code=422, detail="Элементов больше чем ожидалось")

    if not hotel:
        return HTTPException(status_code=404, detail="Элемент не найден")
    return {"status": "OK"}


@router.patch(
    "/{hotel_id}/rooms/{room_id}",
    summary='Частичное обновление данных номера',
    description='<h1>Частично обновляем данные номера</h1>',
)
async def patch_rooms(hotel_id: int, room_id: int, room_data: RoomPatchRequest, db: DBDep):
    _room_data = RoomPatch(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
    try:
        hotel = await db.rooms.edit(_room_data, hotel_id=hotel_id, id=room_id, exclude_unset=True)
        await db.commit()
    except MultipleResultsFound as e:
        return HTTPException(status_code=422, detail="Элементов больше чем ожидалось")

    if not hotel:
        return HTTPException(status_code=404, detail="Элемент не найден")
    return {"status": "OK"}


@router.delete("/{hotel_id}/rooms/{room_id}", summary='Удаление номера')
async def delete_room(hotel_id: int, room_id: int, db: DBDep):
    try:
        hotel = await db.rooms.delete(hotel_id=hotel_id, id=room_id)
        await db.commit()
    except MultipleResultsFound as e:
        return HTTPException(status_code=422, detail="Элементов больше чем ожидалось")

    if not hotel:
        return HTTPException(status_code=404, detail="Элемент не найден")
    return {"status": "OK"}
