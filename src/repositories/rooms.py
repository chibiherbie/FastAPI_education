from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import RoomDataMapper, RoomDataWithRelsMapper
from src.repositories.utils import rooms_ids_for_bookings


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    mapper = RoomDataMapper

    async def get_filtered_by_time(self, hotel_id, date_from: date, date_to: date):
        '''
            with rooms_count as (
                SELECT room_id, count(*) as rooms_booked from bookings
                WHERE date_from <= '2024-09-28' and date_to >= '2024-09-20'
                group by room_id
            ),
            rooms_left_table  as (
                select id as room_id, quantity - coalesce(rooms_booked, 0) as rooms_left
                from rooms
                left outer join rooms_count on rooms.id = rooms_count.room_id
            ) select * from rooms_left_table
            where rooms_left > 0 and room_id in (select id from rooms where hotel_id = 18);
        '''
        rooms_ids_to_get = rooms_ids_for_bookings(date_from, date_to, hotel_id)

        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))
        )
        result = await self.session.execute(query)
        return [RoomDataWithRelsMapper.map_to_domain_entity(model) for model in result.scalars().all()]

    async def get_one_or_none_with_rels(self, **filter_by):
        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter_by(**filter_by)
        )
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if not model:
            return None
        return RoomDataWithRelsMapper.map_to_domain_entity(model)
