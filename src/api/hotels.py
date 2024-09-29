from fastapi import Query, APIRouter, Body, HTTPException
from sqlalchemy.exc import MultipleResultsFound

from src.api.dependecies import PaginationDep, DBDep
from src.shemas.hotels import HotelPatch, HotelAdd

DEFAULT_PER_PAGE = 3

router = APIRouter(prefix='/hotels', tags=['Отели'])


@router.get("", summary='Получение отелей')
async def get_hotels(
        pagination: PaginationDep,
        db: DBDep,
        title: str | None = Query(None, description='Название отеля'),
        location: str | None = Query(None, description='Адрес отеля'),
):
    per_page = pagination.per_page or DEFAULT_PER_PAGE
    return await db.hotels.get_all(
        location=location,
        title=title,
        limit=per_page,
        offset=(pagination.page - 1) * per_page,
    )


@router.get("/{hotel_id}", summary='Получение отеля по id')
async def get_hotel(hotel_id: int, db: DBDep):
    return await db.hotels.get_one_or_none(id=hotel_id)


@router.post("/", summary='Добавление нового отеля')
async def create_hotel(
        db: DBDep,
        hotel_data: HotelAdd = Body(openapi_examples={
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
        }),
):
    hotel = await db.hotels.add(hotel_data)
    await db.commit()

    return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}", summary='Изменение данных об отеле')
async def put_hotel(db: DBDep, hotel_id: int, hotel_data: HotelAdd):
    try:
        hotel = await db.hotels.edit(hotel_data, id=hotel_id)
        await db.commit()
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
async def patch_hotel(db: DBDep, hotel_id: int, hotel_data: HotelPatch):
    try:
        hotel = await db.hotels.edit(hotel_data, id=hotel_id, exclude_unset=True)
        await db.commit()
    except MultipleResultsFound as e:
        return HTTPException(status_code=422, detail="Элементов больше чем ожидалось")

    if not hotel:
        return HTTPException(status_code=404, detail="Элемент не найден")
    return {"status": "OK"}


@router.delete("/{hotel_id}", summary='Удаление отеля')
async def delete_hotel(db: DBDep, hotel_id: int):
    try:
        hotel = await db.hotels.delete(id=hotel_id)
        await db.commit()
    except MultipleResultsFound as e:
        return HTTPException(status_code=422, detail="Элементов больше чем ожидалось")

    if not hotel:
        return HTTPException(status_code=404, detail="Элемент не найден")
    return {"status": "OK"}
