from fastapi import Query, APIRouter, Body, HTTPException
from sqlalchemy.exc import MultipleResultsFound

from src.api.dependecies import PaginationDep
from src.db import async_session_maker
from src.repositories.hotels import HotelsRepository
from src.shemas.hotels import Hotel, HotelPATCH

DEFAULT_PER_PAGE = 3

router = APIRouter(prefix='/hotels', tags=['Отели'])


@router.get("", summary='Получение отелей')
async def get_hotels(
        pagination: PaginationDep,
        title: str | None = Query(None, description='Название отеля'),
        location: str | None = Query(None, description='Адрес отеля'),
):
    per_page = pagination.per_page or DEFAULT_PER_PAGE
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(
            location=location,
            title=title,
            limit=per_page,
            offset=(pagination.page - 1) * per_page,
        )


@router.get("/{hotel_id}", summary='Получение отеля по id')
async def get_hotel(hotel_id: int):
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_one_or_none(id=hotel_id)


@router.post("/", summary='Добавление нового отеля')
async def create_hotel(hotel_data: Hotel = Body(openapi_examples={
    "1": {
        "summary": "Сочи",
        "value": {
            "title": "Отель 5 stars",
            "location": "Сочи, ул. Карт, д. 5",
        }
    },
    "2": {
        "summary": "Дубай",
        "value": {
            "title": "Back one",
            "location": "Думай, ул. Шейха, д. 2, к. 5",
        },
    },
})):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).add(hotel_data)
        await session.commit()

    return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}", summary='Изменение данных об отеле')
async def put_hotel(hotel_id: int, hotel_data: Hotel):
    async with async_session_maker() as session:
        try:
            hotel = await HotelsRepository(session).edit(hotel_data, id=hotel_id)
            await session.commit()
        except MultipleResultsFound as e:
            return HTTPException(status_code=422, detail="Элементов больше чем ожидалось")

    if not hotel:
        return HTTPException(status_code=404, detail="Элемент не найден")
    return {"status": "OK"}


@router.patch(
    "/{hotel_id}",
    summary='Частичное обновление данных об отеле',
    description='<h1>Частично обновляем данные об отеле: можно отправить name, а можно title</h1>',
)
async def patch_hotel(hotel_id: int, hotel_data: HotelPATCH):
    async with async_session_maker() as session:
        try:
            hotel = await HotelsRepository(session).edit(hotel_data, id=hotel_id, exclude_unset=True)
            await session.commit()
        except MultipleResultsFound as e:
            return HTTPException(status_code=422, detail="Элементов больше чем ожидалось")

    if not hotel:
        return HTTPException(status_code=404, detail="Элемент не найден")
    return {"status": "OK"}


@router.delete("/{hotel_id}", summary='Удаление отеля')
async def delete_hotel(hotel_id: int):
    async with async_session_maker() as session:
        try:
            hotel = await HotelsRepository(session).delete(id=hotel_id)
            await session.commit()
        except MultipleResultsFound as e:
            return HTTPException(status_code=422, detail="Элементов больше чем ожидалось")

    if not hotel:
        return HTTPException(status_code=404, detail="Элемент не найден")
    return {"status": "OK"}
