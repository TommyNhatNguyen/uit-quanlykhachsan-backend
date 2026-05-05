from fastapi import APIRouter
from src.db.db import db
from src.models.notification import CreateNotification, UpdateNotification
from src.repositories.notification_repo import NotificationRepository
from src.services.notification_service import NotificationService

router = APIRouter(prefix="/api/notifications", tags=["notifications"])


def _svc() -> NotificationService:
    return NotificationService(NotificationRepository(db))


@router.get("")
def get_list_notifications(page: int = 1, page_size: int = 10):
    return _svc().get_list_notifications(page, page_size)


@router.get("/{id}")
def get_notification(id: int):
    return _svc().get_notification(id)


@router.post("")
def create_notification(notification: CreateNotification):
    return _svc().create_notification(notification)


@router.put("/{id}")
def update_notification(id: int, notification: UpdateNotification):
    data = notification.model_dump()
    data["id"] = id
    return _svc().update_notification(UpdateNotification(**data))


@router.delete("/{id}")
def delete_notification(id: int):
    return _svc().delete_notification(id)
