from fastapi import HTTPException
from fastapi.responses import JSONResponse
from src.models.room import Room, CreateRoom, UpdateRoom
from src.models.paginate_model import PaginateModel
from src.repositories.room_repo import RoomRepository


class RoomService:
    def __init__(self, repo: RoomRepository):
        self.repo = repo

    def get_room(self, room_id: int) -> Room:
        result = self.repo.get_room(room_id)
        if isinstance(result, JSONResponse):
            raise HTTPException(status_code=404, detail=f"Room {room_id} not found")
        return result

    def get_list_rooms(self, page: int = 1, page_size: int = 10) -> PaginateModel[Room]:
        return self.repo.get_list_rooms(page, page_size)

    def create_room(self, room: CreateRoom) -> Room:
        return self.repo.create_room(room)

    def update_room(self, room: UpdateRoom) -> Room:
        current = self.repo.get_room(room.room_id)
        if isinstance(current, JSONResponse):
            raise HTTPException(status_code=404, detail=f"Room {room.room_id} not found")
        merged_data = current.model_dump()
        merged_data.update(room.model_dump(exclude_none=True))
        return self.repo.update_room(UpdateRoom(**merged_data))

    def delete_room(self, room_id: int) -> Room:
        current = self.repo.get_room(room_id)
        if isinstance(current, JSONResponse):
            raise HTTPException(status_code=404, detail=f"Room {room_id} not found")
        self.repo.delete_room(room_id)
        return current
