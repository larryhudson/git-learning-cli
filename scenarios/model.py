from pydantic import BaseModel
from typing import Callable

class Scenario(BaseModel):
    title: str
    difficulty: str
    description: str
    task: str
    hints: list[str]
    generate_func: Callable
    check_func: Callable

    class Config:
        arbitrary_types_allowed = True  # This allows us to use Callable
