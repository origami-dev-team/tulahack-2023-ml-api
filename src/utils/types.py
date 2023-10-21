from pydantic import BaseModel
from typing import TypeVar, Callable, Any, Dict

T = TypeVar("T", bound=BaseModel)
CALLABLE = Callable[..., Any]
DICT = Dict[str, Any]
