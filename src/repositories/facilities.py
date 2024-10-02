from src.models.facilities import FacilitiesOrm
from src.repositories.base import BaseRepository
from src.shemas.facilities import Facilities


class FacilitiesRepository(BaseRepository):
    model = FacilitiesOrm
    schema = Facilities
