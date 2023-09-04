from typing import Any, ClassVar, Union
from typing_extensions import TypedDict
from pydantic import BaseModel

class TableColumn(TypedDict):
    index: int
    name: str
    type: str
    not_null: bool
    default_value: Any
    primary_key: bool

class AbstractDatabase:
    def __init__(self, connection_options: dict = {}) -> None:
        self.connection_options = connection_options
        self.connection = self.connect(connection_options)

    def connect(self, options: dict) -> Any:
        raise NotImplementedError
    
    def exists(self, table: str) -> bool:
        raise NotImplementedError
    
    def create_table(self, name: str, columns: list[tuple[str, str]] = [], if_exists: str = "ignore"):
        raise NotImplementedError
    
    def query(self, query: str) -> list[dict]:
        raise NotImplementedError
    
    def insert(self, table: str, data: dict[str, Any]):
        raise NotImplementedError
    
    def info(self, table: str) -> list[TableColumn]:
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