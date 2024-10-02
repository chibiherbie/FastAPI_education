from fastapi import APIRouter
from src.api.dependecies import DBDep
from src.shemas.facilities import AddFacilities

router = APIRouter(prefix='/facilities', tags=['Удобства'])


@router.get('/')
async def get_facilities(db: DBDep):
    return await db.facilities.get_all()


@router.post('/')
async def create_facility(db: DBDep, data: AddFacilities):
    facilities = await db.facilities.add(data)
    await db.commit()
    return facilities
