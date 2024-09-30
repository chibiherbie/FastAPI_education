from datetime import date

from sqlalchemy import select, func

from src.models.bookings import BookingsOrm
from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.shemas.rooms import Room


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room

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
        rooms_count = (
            select(BookingsOrm.room_id, func.count("*").label("rooms_booked"))
            .select_from(BookingsOrm)
            .filter(
                BookingsOrm.date_from <= date_to,
                BookingsOrm.date_to >= date_from,
            )
            .group_by(BookingsOrm.room_id)
            .cte(name="rooms_count")
        )

        rooms_left_table = (
            select(
                RoomsOrm.id.label("room_id"),
                (RoomsOrm.quantity - func.coalesce(rooms_count.c.rooms_booked, 0)).label("rooms_left"),
                # rooms_count.c - "c" это label
            )
            .select_from(RoomsOrm)
            .outerjoin(rooms_count, rooms_count.c.room_id == RoomsOrm.id)
            .cte(name="rooms_left_table")
        )

        rooms_id_for_hotel = (
            select(RoomsOrm.id)
            .select_from(RoomsOrm)
            .filter_by(hotel_id=hotel_id)
            .subquery(name="rooms_id_for_hotel")  # является подзапросом
        )

        rooms_ids_to_get = (
            select(rooms_left_table.c.room_id)
            .select_from(rooms_left_table)
            .filter(
                rooms_left_table.c.rooms_left > 0,
                rooms_left_table.c.room_id.in_(rooms_id_for_hotel)
            )
        )

        return await self.get_filtered(RoomsOrm.id.in_(rooms_ids_to_get))
