from fastapi import Query, APIRouter, Body, HTTPException
from sqlalchemy.exc import MultipleResultsFound

from src.db import async_session_maker
from src.repositories.rooms import RoomsRepository
from src.shemas.rooms import Room, RoomPATCH, RoomAdd

DEFAULT_PER_PAGE = 3

router = APIRouter(prefix='/hotels', tags=['Комнаты'])


@router.get("/{hotel_id}/rooms", summary='Получение комнат')
async def get_rooms(
        hotel_id: int,
        title: str | None = Query(None, description='Название комнаты'),
        description: str | None = Query(None, description='Описание комнаты'),
        price: int | None = Query(None, description='Стоимость аренды комнаты'),
        quantity: int | None = Query(None, description='Количество комнат в отеле'),
):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_all(
            hotel_id=hotel_id,
            title=title,
            description=description,
            price=price,
            quantity=quantity,
        )


@router.get("/{hotel_id}/rooms/{room_id}", summary='Получение комнаты в отеле по id')
async def get_room(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_one_or_none(hotel_id=hotel_id, id=room_id)


@router.post("/{hotel_id}/rooms/", summary='Добавление новой комнаты')
async def create_room(
        hotel_id: int,
        room_data: RoomAdd = Body(openapi_examples={
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
    async with async_session_maker() as session:
        room = await RoomsRepository(session).add(room_data, hotel_id=hotel_id)
        await session.commit()

    return {"status": "OK", "data": room}


@router.put("/{hotel_id}/rooms/{room_id}", summary='Изменение данных в комнате')
async def put_room(hotel_id: int, room_id: int, room_data: RoomAdd):
    async with async_session_maker() as session:
        try:
            hotel = await RoomsRepository(session).edit(room_data, hotel_id=hotel_id, id=room_id)
            await session.commit()
        except MultipleResultsFound as e:
            return HTTPException(status_code=422, detail="Элементов больше чем ожидалось")

    if not hotel:
        return HTTPException(status_code=404, detail="Элемент не найден")
    return {"status": "OK"}


@router.patch(
    "/{hotel_id}/rooms/{room_id}",
    summary='Частичное обновление данных комнаты',
    description='<h1>Частично обновляем данные комнаты</h1>',
)
async def patch_rooms(hotel_id: int, room_id: int, room_data: RoomPATCH):
    async with async_session_maker() as session:
        try:
            hotel = await RoomsRepository(session).edit(room_data, hotel_id=hotel_id, id=room_id, exclude_unset=True)
            await session.commit()
        except MultipleResultsFound as e:
            return HTTPException(status_code=422, detail="Элементов больше чем ожидалось")

    if not hotel:
        return HTTPException(status_code=404, detail="Элемент не найден")
    return {"status": "OK"}


@router.delete("/{hotel_id}/rooms/{room_id}", summary='Удаление комнаты')
async def delete_room(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        try:
            hotel = await RoomsRepository(session).delete(hotel_id=hotel_id, id=room_id)
            await session.commit()
        except MultipleResultsFound as e:
            return HTTPException(status_code=422, detail="Элементов больше чем ожидалось")

    if not hotel:
        return HTTPException(status_code=404, detail="Элемент не найден")
    return {"status": "OK"}
