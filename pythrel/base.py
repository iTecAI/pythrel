from typing import Any, ClassVar
from pydantic import BaseModel

class AbstractDatabase:
    def __init__(self, connection_options: dict = {}) -> None:
        self.connection_options = connection_options
        self.connection = self.connect(connection_options)

    def connect(self, options: dict) -> Any:
        raise NotImplementedError
    
    def create_table(self, name: str, columns: list[tuple[str, str]] = [], if_exists: str = "ignore"):
        raise NotImplementedError
    
    def get_table(self, table: str, columns: list[str] = "*", where: str = None) -> list[dict]:
        raise NotImplementedError
    
    def query(self, query: str) -> list[dict]:
        raise NotImplementedError
    
    def orm(self, base_query: list[str]):
        def orm_decorator(cls):
            cls.database = self
            cls.base_query = base_query

            def _cls_load(cls, query: list[str]) -> list:
                return [cls(**record) for record in cls.database.query([*cls.base_query, *query])]

            cls.load = classmethod(_cls_load)
            return cls
        return orm_decorator
    
class Record(BaseModel):
    database: ClassVar[AbstractDatabase]
    base_query: ClassVar[str]
    
    @classmethod
    def load(cls, query: list[str]) -> list:
        raise NotImplementedError