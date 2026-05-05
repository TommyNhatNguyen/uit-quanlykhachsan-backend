from fastapi import HTTPException
from fastapi.responses import JSONResponse
from src.models.counter import Counter, CreateCounter, UpdateCounter
from src.models.paginate_model import PaginateModel
from src.repositories.counter_repo import CounterRepository


class CounterService:
    def __init__(self, repo: CounterRepository):
        self.repo = repo

    def get_counter(self, name: str) -> Counter:
        result = self.repo.get_counter(name)
        if isinstance(result, JSONResponse):
            raise HTTPException(status_code=404, detail=f"Counter '{name}' not found")
        return result

    def get_list_counters(self, page: int = 1, page_size: int = 10) -> PaginateModel[Counter]:
        return self.repo.get_list_counters(page, page_size)

    def create_counter(self, counter: CreateCounter) -> Counter:
        return self.repo.create_counter(counter)

    def update_counter(self, counter: UpdateCounter) -> Counter:
        current = self.repo.get_counter(counter.name)
        if isinstance(current, JSONResponse):
            raise HTTPException(status_code=404, detail=f"Counter '{counter.name}' not found")
        merged_data = current.model_dump()
        merged_data.update(counter.model_dump(exclude_none=True))
        return self.repo.update_counter(UpdateCounter(**merged_data))

    def delete_counter(self, name: str) -> Counter:
        current = self.repo.get_counter(name)
        if isinstance(current, JSONResponse):
            raise HTTPException(status_code=404, detail=f"Counter '{name}' not found")
        self.repo.delete_counter(name)
        return current
