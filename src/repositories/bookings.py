from sqlalchemy import select, func

from src.models.bookings import BookingsOrm
from src.repositories.base import BaseRepository
from src.shemas.bookings import Booking


class BookingsRepository(BaseRepository):
    model = BookingsOrm
    schema = Booking
