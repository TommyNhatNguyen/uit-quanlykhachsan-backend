from fastapi import APIRouter
from src.db.db import db
from src.models.counter import CreateCounter, UpdateCounter
from src.repositories.counter_repo import CounterRepository
from src.services.counter_service import CounterService

router = APIRouter(prefix="/api/counters", tags=["counters"])


def _svc() -> CounterService:
    return CounterService(CounterRepository(db))


@router.get("")
def get_list_counters(page: int = 1, page_size: int = 10):
    return _svc().get_list_counters(page, page_size)


@router.get("/{name}")
def get_counter(name: str):
    return _svc().get_counter(name)


@router.post("")
def create_counter(counter: CreateCounter):
    return _svc().create_counter(counter)


@router.put("/{name}")
def update_counter(name: str, counter: UpdateCounter):
    data = counter.model_dump()
    data["name"] = name
    return _svc().update_counter(UpdateCounter(**data))


@router.delete("/{name}")
def delete_counter(name: str):
    return _svc().delete_counter(name)
