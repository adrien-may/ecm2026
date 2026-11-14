from datetime import datetime, timezone

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    done: Mapped[bool] = mapped_column(default=False)
    # ISO 8601 UTC string: SQLite does not preserve timezone-aware datetimes.
    creation_date: Mapped[str] = mapped_column(
        default=lambda: datetime.now(timezone.utc).isoformat()
    )

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "done": self.done,
            "creation_date": self.creation_date,
        }
