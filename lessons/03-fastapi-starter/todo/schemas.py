from typing import Annotated

from pydantic import BaseModel, ConfigDict, StringConstraints


Title = Annotated[str, StringConstraints(
    strip_whitespace=True, min_length=1, max_length=255, strict=True,
)]


class TaskCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    title: Title


class TaskRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    done: bool
    creation_date: str
