from pydantic import BaseModel


class Hotel(BaseModel):
    title: str
    name: str


class HotelPATCH(BaseModel):
    title: str | None = None  # Field(None)
    name: str | None = None
