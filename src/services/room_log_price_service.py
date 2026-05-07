from fastapi import HTTPException
from fastapi.responses import JSONResponse
from src.models.room_price_log import QueryRoomPriceLogsParams, RoomPriceLog, CreateRoomPriceLog, UpdateRoomPriceLog
from src.repositories.room_log_price_repo import RoomPriceLogRepository


class RoomPriceLogService:
    def __init__(self, repo: RoomPriceLogRepository):
        self.repo = repo

    def get_room_price_log(self, id: int) -> RoomPriceLog:
        result = self.repo.get_room_price_log(id)
        if isinstance(result, JSONResponse):
            raise HTTPException(status_code=404, detail=f"RoomPriceLog {id} not found")
        return result

    def get_list_room_price_logs(self, params: QueryRoomPriceLogsParams) -> dict:
        return self.repo.get_list_room_price_logs(params)

    def create_room_price_log(self, log: CreateRoomPriceLog) -> RoomPriceLog:
        return self.repo.create_room_price_log(log)

    def update_room_price_log(self, id: int, data: UpdateRoomPriceLog) -> RoomPriceLog:
        current = self.repo.get_room_price_log(id)
        if isinstance(current, JSONResponse):
            raise HTTPException(status_code=404, detail=f"RoomPriceLog {id} not found")
        merged = {**current.model_dump(), **data.model_dump(exclude_none=True)}
        return self.repo.update_room_price_log(id, RoomPriceLog(**merged))

    def delete_room_price_log(self, id: int) -> RoomPriceLog:
        current = self.repo.get_room_price_log(id)
        if isinstance(current, JSONResponse):
            raise HTTPException(status_code=404, detail=f"RoomPriceLog {id} not found")
        self.repo.delete_room_price_log(id)
        return current
