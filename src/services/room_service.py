from ast import List
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from src.models.room import QueryRoomsParams, Room, CreateRoom, UpdateRoom, UpdateRoomPrice
from src.models.room_price_log import CreateRoomPriceLog, RoomPriceLog
from src.repositories.room_repo import RoomRepository
from src.services.room_log_price_service import RoomPriceLogService


class RoomService:
    def __init__(self, repo: RoomRepository, roomPriceLogSerivce : RoomPriceLogService):
        self.repo = repo
        self.roomPriceLogSerivce = roomPriceLogSerivce

    def get_room(self, id: int) -> Room:
        result = self.repo.get_room(id)
        if isinstance(result, JSONResponse):
            raise HTTPException(status_code=404, detail=f"Room {id} not found")
        return result

    def get_list_rooms(self, params: QueryRoomsParams) -> dict:
        return self.repo.get_list_rooms(params)

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

    def update_room_price(self, payload: UpdateRoomPrice) -> Room:
        current = self.repo.get_room(payload.room_id)
        if isinstance(current, JSONResponse):
            raise HTTPException(status_code=404, detail=f"Room {id} not found")
        
        updatedRoomPayload = UpdateRoom(current_price_per_night=payload.price_per_night)
        mergedRoom = {**current.model_dump(),**updatedRoomPayload.model_dump(exclude_none=True)}
        result = self.repo.update_room(payload.room_id, Room(**mergedRoom))
        return result

    def get_room_history_prices(self, id: int):
            return self.repo.get_room_history_prices(id) 