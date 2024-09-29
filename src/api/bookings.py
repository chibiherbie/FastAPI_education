from fastapi import Query, APIRouter, Body, HTTPException, Request
from sqlalchemy.exc import MultipleResultsFound

from src.api.dependecies import PaginationDep, DBDep, UserIdDep
from src.shemas.bookings import Booking, BookingAddRequest, BookingAdd
from src.shemas.hotels import HotelPatch, HotelAdd
from src.shemas.rooms import Room

DEFAULT_PER_PAGE = 3

router = APIRouter(prefix='/bookings', tags=['Бронирование'])


@router.post('/')
async def create_booking(db: DBDep, data_booking: BookingAddRequest, user_id: UserIdDep):

    if data_booking.date_to >= data_booking.date_from:  # TODO проверять на будущую дату и не занят ли номер
        raise HTTPException(status_code=400, detail='Несоответствующая дата бронирования')

    room: Room = await db.rooms.get_one_or_none(id=data_booking.room_id)
    if not room:
        raise HTTPException(status_code=404, detail='Такой комнаты нет')

    _data_booking = BookingAdd(user_id=user_id, price=room.price, **data_booking.model_dump())
    booking = await db.bookings.add(_data_booking)
    await db.commit()

    return booking
