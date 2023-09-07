import inspect
from typing import ClassVar, Any
from pydantic import BaseModel

class RelORM(BaseModel):
    database: ClassVar[Any]
    def __init__(self, database, **data) -> None:
        super().__init__(database=database, **data)
