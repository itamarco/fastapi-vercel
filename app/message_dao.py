from typing import List, Optional
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import select

from app.db import get_session
from app.models import MessageResponse
from app.schema import Message

class MessageDAO:
    @staticmethod
    def create(message: str) -> MessageResponse:
        """Create a new message."""
        try:
            with get_session() as session:
                db_message = Message(message=message)
                session.add(db_message)
                session.commit()
                session.refresh(db_message)
                return MessageResponse(**db_message.model_dump())
        except SQLAlchemyError as e:
            raise RuntimeError(f"Failed to create message: {str(e)}") from e

    @staticmethod
    def get_by_id(message_id: int) -> Optional[Message]:
        """Retrieve a message by its ID."""
        try:
            with get_session() as session:
                statement = select(Message).where(Message.id == message_id)
                result = session.exec(statement).first()
                return result
        except SQLAlchemyError as e:
            raise RuntimeError(f"Failed to retrieve message: {str(e)}") from e

    @staticmethod
    def get_all(limit: int = 100, offset: int = 0) -> List[MessageResponse]:
        """Retrieve all messages with pagination."""
        try:
            with get_session() as session:
                statement = (
                    select(Message)
                    .offset(offset)
                    .limit(limit)
                )
                msgs = list(session.exec(statement))
                return [MessageResponse(**msg.model_dump()) for msg in msgs]
        except SQLAlchemyError as e:
            raise RuntimeError(f"Failed to retrieve messages: {str(e)}") from e

