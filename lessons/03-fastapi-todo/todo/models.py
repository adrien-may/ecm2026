from datetime import UTC, datetime

from sqlmodel import Field
from .schemas import TaskBase


class Task(TaskBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    done: bool = False
    creation_date: str = Field(
        default_factory=lambda: datetime.now(UTC).isoformat()
    )
