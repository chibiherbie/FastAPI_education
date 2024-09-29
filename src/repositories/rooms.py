from sqlalchemy import select, func

from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.shemas.rooms import Room


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room

    async def get_all(self, hotel_id, title, description, price, quantity) -> list[Room]:

        query = select(RoomsOrm).where(RoomsOrm.hotel_id == hotel_id)
        if title:
            query = query.filter(func.lower(RoomsOrm.title).contains(title.strip().lower()))
        if description:
            query = query.filter(func.lower(RoomsOrm.description).contains(description.strip().lower()))
        if price:
            query = query.filter(RoomsOrm.price == price)
        if quantity:
            query = query.filter(RoomsOrm.quantity == quantity)

        # query = (
        #     query
        #     .where(hotel_id=hotel_id)
        # )
        result = await self.session.execute(query)
        return [Room.model_validate(hotel, from_attributes=True) for hotel in result.scalars().all()]
