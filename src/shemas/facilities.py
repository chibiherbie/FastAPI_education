from pydantic import BaseModel


class AddFacilities(BaseModel):
    title: str


class Facilities(AddFacilities):
    id: int

