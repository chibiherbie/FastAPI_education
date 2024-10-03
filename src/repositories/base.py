from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import select, insert, delete, update
from sqlalchemy.exc import IntegrityError


class BaseRepository:
    model = None
    schema: BaseModel = None

    def __init__(self, session):
        self.session = session

    async def get_filtered(self, *filter, **filter_by):
        query = (
            select(self.model)
            .filter(*filter)
            .filter_by(**filter_by)
        )
        result = await self.session.execute(query)
        return [self.schema.model_validate(model, from_attributes=True) for model in result.scalars().all()]

    async def get_all(self, *args, **kwargs):
        return await self.get_filtered()

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if not model:
            return None
        return self.schema.model_validate(model, from_attributes=True)

    async def add(self, data: BaseModel):
        try:
            add_data_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
            result = await self.session.execute(add_data_stmt)
            model = result.scalars().one()
            return self.schema.model_validate(model, from_attributes=True)
        except IntegrityError as e:
            if 'ForeignKeyViolationError' in str(e):
                raise HTTPException(status_code=400, detail='Такого отеля нет')
            raise HTTPException(status_code=400)

    async def add_bulk(self, data: list[BaseModel]):
        add_data_stmt = insert(self.model).values([item.model_dump() for item in data]).returning(self.model)
        await self.session.execute(add_data_stmt)

    async def edit(self, data: BaseModel, exclude_unset: bool = False, **filter_by):
        update_data_stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=exclude_unset))
            .returning(self.model)
        )
        result = await self.session.execute(update_data_stmt)
        return result.scalar()

    async def delete(self, **filter_by):
        delete_data_stmt = delete(self.model).filter_by(**filter_by).returning(self.model)
        result = await self.session.execute(delete_data_stmt)
        return result.scalar()

    async def delete_bulk(self, *args):
        delete_data_stmt = delete(self.model).filter(*args)
        await self.session.execute(delete_data_stmt)
