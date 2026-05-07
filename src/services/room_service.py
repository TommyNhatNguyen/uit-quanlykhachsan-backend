from fastapi import HTTPException
from fastapi.responses import JSONResponse
from src.models.room import Room, CreateRoom, UpdateRoom
from src.repositories.room_repo import RoomRepository


class RoomService:
    def __init__(self, repo: RoomRepository):
        self.repo = repo

    def get_room(self, id: int) -> Room:
        result = self.repo.get_room(id)
        if isinstance(result, JSONResponse):
            raise HTTPException(status_code=404, detail=f"Room {id} not found")
        return result

    def get_list_rooms(self, page: int = 1, page_size: int = 10) -> dict:
        return self.repo.get_list_rooms(page, page_size)

    def create_room(self, room: CreateRoom) -> Room:
        return self.repo.create_room(room)

    def update_room(self, id: int, data: UpdateRoom) -> Room:
        current = self.repo.get_room(id)
        if isinstance(current, JSONResponse):
            raise HTTPException(status_code=404, detail=f"Room {id} not found")
        merged = {**current.model_dump(), **data.model_dump(exclude_none=True)}
        return self.repo.update_room(id, Room(**merged))

    def delete_room(self, id: int) -> Room:
        current = self.repo.get_room(id)
        if isinstance(current, JSONResponse):
            raise HTTPException(status_code=404, detail=f"Room {id} not found")
        self.repo.delete_room(id)
        return current
