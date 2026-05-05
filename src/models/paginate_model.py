from typing import Generic, List
from pydantic import BaseModel


class PaginateModel[T](BaseModel, Generic[T]):
    page: int
    page_size: int
    total: int
    total_pages: int
    data: List[T]
