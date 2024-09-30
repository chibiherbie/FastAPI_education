from datetime import date

from sqlalchemy import select, func

from src.models.hotels import HotelsOrm
from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.repositories.utils import rooms_ids_for_bookings
from src.shemas.hotels import Hotel


class HotelsRepository(BaseRepository):
    model = HotelsOrm
    schema = Hotel

    async def get_filtered_by_time(
            self,
            date_from: date,
            date_to: date,
            location: str,
            title: str,
            limit: int,
            offset: int,
    ):
        rooms_ids_to_get = rooms_ids_for_bookings(date_from, date_to)
        hotels_ids_to_get = (
            select(RoomsOrm.hotel_id)
            .select_from(RoomsOrm)
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))
        )

        filters = [HotelsOrm.id.in_(hotels_ids_to_get)]
        if location:
            filters.append(func.lower(HotelsOrm.location).contains(location.strip().lower()))
        if title:
            filters.append(func.lower(HotelsOrm.title).contains(title.strip().lower()))

        query = (
            select(self.model)
            .filter(*filters)
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(query)
        return [self.schema.model_validate(model, from_attributes=True) for model in result.scalars().all()]
