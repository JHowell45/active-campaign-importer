from typing import TypeVar

from pydantic import BaseModel, Field, computed_field

from app.importer.models.tasks import Task

T = TypeVar("T")


class Meta(BaseModel):
    total: int


class TaskResponse(BaseModel):
    meta: Meta
    data: list[Task] = Field(alias="dealTasks")

    @computed_field  # type: ignore[prop-decorator]
    @property
    def count(self) -> int:
        return len(self.data)
