from fastapi import HTTPException
from fastapi.responses import JSONResponse
from src.models.room_log_price import RoomLogPrice, CreateRoomLogPrice, UpdateRoomLogPrice
from src.models.paginate_model import PaginateModel
from src.repositories.room_log_price_repo import RoomLogPriceRepository


class RoomLogPriceService:
    def __init__(self, repo: RoomLogPriceRepository):
        self.repo = repo

    def get_room_log_price(self, id: int) -> RoomLogPrice:
        result = self.repo.get_room_log_price(id)
        if isinstance(result, JSONResponse):
            raise HTTPException(status_code=404, detail=f"RoomLogPrice {id} not found")
        return result

    def get_list_room_log_prices(self, page: int = 1, page_size: int = 10) -> PaginateModel[RoomLogPrice]:
        return self.repo.get_list_room_log_prices(page, page_size)

    def create_room_log_price(self, log: CreateRoomLogPrice) -> RoomLogPrice:
        return self.repo.create_room_log_price(log)

    def update_room_log_price(self, log: UpdateRoomLogPrice) -> RoomLogPrice:
        current = self.repo.get_room_log_price(log.id)
        if isinstance(current, JSONResponse):
            raise HTTPException(status_code=404, detail=f"RoomLogPrice {log.id} not found")
        merged_data = current.model_dump()
        merged_data.update(log.model_dump(exclude_none=True))
        return self.repo.update_room_log_price(UpdateRoomLogPrice(**merged_data))

    def delete_room_log_price(self, id: int) -> RoomLogPrice:
        current = self.repo.get_room_log_price(id)
        if isinstance(current, JSONResponse):
            raise HTTPException(status_code=404, detail=f"RoomLogPrice {id} not found")
        self.repo.delete_room_log_price(id)
        return current
