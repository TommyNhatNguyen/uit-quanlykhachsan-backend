from fastapi import HTTPException
from fastapi.responses import JSONResponse
from src.models.room_inventory import RoomInventory, CreateRoomInventory, UpdateRoomInventory
from src.models.paginate_model import PaginateModel
from src.repositories.room_inventory_repo import RoomInventoryRepository


class RoomInventoryService:
    def __init__(self, repo: RoomInventoryRepository):
        self.repo = repo

    def get_room_inventory(self, room_id: int) -> RoomInventory:
        result = self.repo.get_room_inventory(room_id)
        if isinstance(result, JSONResponse):
            raise HTTPException(status_code=404, detail=f"RoomInventory for room {room_id} not found")
        return result

    def get_list_room_inventories(self, page: int = 1, page_size: int = 10) -> PaginateModel[RoomInventory]:
        return self.repo.get_list_room_inventories(page, page_size)

    def create_room_inventory(self, room_inventory: CreateRoomInventory) -> RoomInventory:
        return self.repo.create_room_inventory(room_inventory)

    def update_room_inventory(self, room_inventory: UpdateRoomInventory) -> RoomInventory:
        current = self.repo.get_room_inventory(room_inventory.room_id)
        if isinstance(current, JSONResponse):
            raise HTTPException(status_code=404, detail=f"RoomInventory for room {room_inventory.room_id} not found")
        merged_data = current.model_dump()
        merged_data.update(room_inventory.model_dump(exclude_none=True))
        return self.repo.update_room_inventory(UpdateRoomInventory(**merged_data))

    def delete_room_inventory(self, room_id: int) -> RoomInventory:
        current = self.repo.get_room_inventory(room_id)
        if isinstance(current, JSONResponse):
            raise HTTPException(status_code=404, detail=f"RoomInventory for room {room_id} not found")
        self.repo.delete_room_inventory(room_id)
        return current
