
from typing import TypedDict


class TodoDict(TypedDict):
    todo_id: int
    todo_text: str
    is_complete: bool
