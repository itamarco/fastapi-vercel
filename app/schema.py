from sqlmodel import SQLModel, Field

class Message(SQLModel, table=True):
    __tablename__ = 'messages'

    id: int = Field(
        default=None,
        primary_key=True,
        nullable=False,
        index=True
    )
    message: str = Field(nullable=False)


