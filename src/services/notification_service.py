from fastapi import HTTPException
from fastapi.responses import JSONResponse
from src.models.notification import Notification, CreateNotification, UpdateNotification
from src.repositories.notification_repo import NotificationRepository


class NotificationService:
    def __init__(self, repo: NotificationRepository):
        self.repo = repo

    def get_notification(self, id: int) -> Notification:
        result = self.repo.get_notification(id)
        if isinstance(result, JSONResponse):
            raise HTTPException(status_code=404, detail=f"Notification {id} not found")
        return result

    def get_list_notifications(self, page: int = 1, page_size: int = 10) -> dict:
        return self.repo.get_list_notifications(page, page_size)

    def create_notification(self, notification: CreateNotification) -> Notification:
        return self.repo.create_notification(notification)

    def update_notification(self, notification: UpdateNotification) -> Notification:
        current = self.repo.get_notification(notification.id)
        if isinstance(current, JSONResponse):
            raise HTTPException(status_code=404, detail=f"Notification {notification.id} not found")
        merged_data = current.model_dump()
        merged_data.update(notification.model_dump(exclude_none=True))
        return self.repo.update_notification(UpdateNotification(**merged_data))

    def delete_notification(self, id: int) -> Notification:
        current = self.repo.get_notification(id)
        if isinstance(current, JSONResponse):
            raise HTTPException(status_code=404, detail=f"Notification {id} not found")
        self.repo.delete_notification(id)
        return current
