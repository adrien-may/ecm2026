from typing import Annotated

from pydantic import BaseModel, ConfigDict, StrictBool, StringConstraints, model_validator


Title = Annotated[str, StringConstraints(
    strip_whitespace=True, min_length=1, max_length=255, strict=True,
)]


class TaskCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    title: Title


class TaskPatch(BaseModel):
    model_config = ConfigDict(extra="forbid")
    title: Title | None = None
    done: StrictBool | None = None

    @model_validator(mode="after")
    def require_nonempty_nonnull_fields(self):
        if not self.model_fields_set:
            raise ValueError("At least one field is required")
        for field in self.model_fields_set:
            if getattr(self, field) is None:
                raise ValueError(f"{field} cannot be null")
        return self


class TaskRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    done: bool
    creation_date: str
