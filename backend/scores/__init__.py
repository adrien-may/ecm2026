from datetime import datetime, timezone
from pathlib import Path
from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict, Field, StringConstraints
from sqlalchemy import create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column


class Base(DeclarativeBase):
    pass


class Score(Base):
    __tablename__ = "score"
    id: Mapped[int] = mapped_column(primary_key=True)
    player: Mapped[str]
    points: Mapped[int]
    created_at: Mapped[str] = mapped_column(default=lambda: datetime.now(timezone.utc).isoformat())


class ScoreCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    player: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=24, strict=True)]
    points: Annotated[int, Field(strict=True, ge=0, le=90)]


class ScoreRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    player: str
    points: int
    created_at: str


def create_app(database_url=None):
    if database_url is None:
        folder = Path(__file__).resolve().parent.parent / "instance"
        folder.mkdir(exist_ok=True)
        database_url = f"sqlite:///{folder / 'scores.sqlite'}"
    engine = create_engine(database_url, connect_args={"check_same_thread": False})
    # Supplied project setup. create_all creates missing tables, not migrations.
    Base.metadata.create_all(engine)
    app = FastAPI(title="ECM · Scores")
    app.state.engine = engine
    app.add_middleware(CORSMiddleware,
        allow_origins=["http://localhost:5175", "http://127.0.0.1:5175"],
        allow_methods=["GET", "POST"], allow_headers=["Content-Type"])

    def get_session():
        with Session(engine) as session:
            yield session

    DatabaseSession = Annotated[Session, Depends(get_session)]

    @app.get("/scores/", response_model=list[ScoreRead])
    def list_scores(session: DatabaseSession):
        return session.scalars(select(Score).order_by(Score.points.desc(), Score.id).limit(10)).all()

    @app.post("/scores/", response_model=ScoreRead, status_code=201)
    def save_score(data: ScoreCreate, session: DatabaseSession):
        score = Score(**data.model_dump())
        session.add(score)
        session.commit()
        session.refresh(score)
        return score

    return app
