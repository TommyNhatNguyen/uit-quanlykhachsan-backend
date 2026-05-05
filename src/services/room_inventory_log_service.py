from fastapi import HTTPException
from fastapi.responses import JSONResponse
from src.models.room_inventory_log import RoomInventoryLog, CreateRoomInventoryLog, UpdateRoomInventoryLog
from src.repositories.room_inventory_log_repo import RoomInventoryLogRepository


class RoomInventoryLogService:
    def __init__(self, repo: RoomInventoryLogRepository):
        self.repo = repo

    def get_room_inventory_log(self, id: int) -> RoomInventoryLog:
        result = self.repo.get_room_inventory_log(id)
        if isinstance(result, JSONResponse):
            raise HTTPException(status_code=404, detail=f"RoomInventoryLog {id} not found")
        return result

    def get_list_room_inventory_logs(self, page: int = 1, page_size: int = 10) -> dict:
        return self.repo.get_list_room_inventory_logs(page, page_size)

    def create_room_inventory_log(self, log: CreateRoomInventoryLog) -> RoomInventoryLog:
        return self.repo.create_room_inventory_log(log)

    def update_room_inventory_log(self, log: UpdateRoomInventoryLog) -> RoomInventoryLog:
        current = self.repo.get_room_inventory_log(log.id)
        if isinstance(current, JSONResponse):
            raise HTTPException(status_code=404, detail=f"RoomInventoryLog {log.id} not found")
        merged_data = current.model_dump()
        merged_data.update(log.model_dump(exclude_none=True))
        return self.repo.update_room_inventory_log(UpdateRoomInventoryLog(**merged_data))

    def delete_room_inventory_log(self, id: int) -> RoomInventoryLog:
        current = self.repo.get_room_inventory_log(id)
        if isinstance(current, JSONResponse):
            raise HTTPException(status_code=404, detail=f"RoomInventoryLog {id} not found")
        self.repo.delete_room_inventory_log(id)
        return current
