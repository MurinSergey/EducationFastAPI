from typing import Annotated
from fastapi import Depends, Query
from pydantic import BaseModel


class PaginationParameters(BaseModel):
    page: Annotated[int | None, Query(default=1, ge=1)]
    per_page: Annotated[int | None, Query(default=None, ge=1, le=30)]

PaginationDep = Annotated[PaginationParameters, Depends()]