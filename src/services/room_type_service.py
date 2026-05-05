from fastapi import HTTPException
from fastapi.responses import JSONResponse
from src.models.room_type import RoomType, CreateRoomType, UpdateRoomType
from src.repositories.room_type_repo import RoomTypeRepository


class RoomTypeService:
    def __init__(self, repo: RoomTypeRepository):
        self.repo = repo

    def get_room_type(self, room_type_id: int) -> RoomType:
        result = self.repo.get_room_type(room_type_id)
        if isinstance(result, JSONResponse):
            raise HTTPException(status_code=404, detail=f"RoomType {room_type_id} not found")
        return result

    def get_list_room_types(self, page: int = 1, page_size: int = 10) -> dict:
        return self.repo.get_list_room_types(page, page_size)

    def create_room_type(self, room_type: CreateRoomType) -> RoomType:
        return self.repo.create_room_type(room_type)

    def update_room_type(self, room_type: UpdateRoomType) -> RoomType:
        current = self.repo.get_room_type(room_type.room_type_id)
        if isinstance(current, JSONResponse):
            raise HTTPException(status_code=404, detail=f"RoomType {room_type.room_type_id} not found")
        merged_data = current.model_dump()
        merged_data.update(room_type.model_dump(exclude_none=True))
        return self.repo.update_room_type(UpdateRoomType(**merged_data))

    def delete_room_type(self, room_type_id: int) -> RoomType:
        current = self.repo.get_room_type(room_type_id)
        if isinstance(current, JSONResponse):
            raise HTTPException(status_code=404, detail=f"RoomType {room_type_id} not found")
        self.repo.delete_room_type(room_type_id)
        return current
