from pydantic import BaseModel, Field


class TaskIn(BaseModel):
    title: str = Field(max_length=50)
    description: str = Field(max_length=200)
    done: bool = Field(False)


class Task(TaskIn):
    id: int
