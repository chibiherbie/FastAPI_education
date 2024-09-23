from fastapi import Depends, Query
from pydantic import BaseModel

from typing import Annotated

DEFAULT_PAGE = 1


class PaginationParams(BaseModel):
    page: Annotated[int, Query(DEFAULT_PAGE, ge=1, description='Номер страницы откуда брать отели для пагинации')]
    per_page: Annotated[int | None, Query(None, ge=1, le=100, description='Количество возвращенных отелей')]


PaginationDep = Annotated[PaginationParams, Depends()]
