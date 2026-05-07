from fastapi import HTTPException
from fastapi.responses import JSONResponse
from src.models.room_type import RoomType, CreateRoomType, UpdateRoomType
from src.repositories.room_type_repo import RoomTypeRepository


class RoomTypeService:
    def __init__(self, repo: RoomTypeRepository):
        self.repo = repo

    def get_room_type(self, id: int) -> RoomType:
        result = self.repo.get_room_type(id)
        if isinstance(result, JSONResponse):
            raise HTTPException(status_code=404, detail=f"RoomType {id} not found")
        return result

    def get_list_room_types(self, page: int = 1, page_size: int = 10) -> dict:
        result = self.repo.get_list_room_types(page, page_size)
        if isinstance(result, JSONResponse):
            raise HTTPException(status_code=500, detail=result["error"])
        return result

    def create_room_type(self, room_type: CreateRoomType) -> RoomType:
        return self.repo.create_room_type(room_type)

    def update_room_type(self, id: int, data: UpdateRoomType) -> RoomType:
        current = self.repo.get_room_type(id)
        if isinstance(current, JSONResponse):
            raise HTTPException(status_code=404, detail=f"RoomType {id} not found")
        merged = {**current.model_dump(), **data.model_dump(exclude_none=True)}
        return self.repo.update_room_type(id, RoomType(**merged))

    def delete_room_type(self, id: int) -> RoomType:
        current = self.repo.get_room_type(id)
        if isinstance(current, JSONResponse):
            raise HTTPException(status_code=404, detail=f"RoomType {id} not found")
        self.repo.delete_room_type(id)
        return current
