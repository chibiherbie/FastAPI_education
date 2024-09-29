from datetime import date
from pydantic import BaseModel, ConfigDict


class BookingAddRequest(BaseModel):
    room_id: int
    date_to: date
    date_from: date


class BookingAdd(BaseModel):
    user_id: int
    room_id: int
    date_to: date
    date_from: date
    price: int


class Booking(BookingAdd):
    id: int
