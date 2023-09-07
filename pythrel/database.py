from typing import Any, Union, Literal

class RelDatabase:
    def __init__(self, connection_args: dict = {}) -> None:
        self.connection_args = connection_args

    def execute(self, query: str, commit: bool = False) -> list[dict[str, Any]]:
        raise NotImplementedError
    
    def commit(self) -> None:
        raise NotImplementedError
    
    def rollback(self) -> None:
        raise NotImplementedError
    
    def get_table(self, table: str, columns: Union[list[str], Literal["*"]] = "*") -> list[dict[str, Any]]:
        raise NotImplementedError
    
    def get_columns(self, columns: dict[str, list[str]], primary: str) -> list[dict[str, Any]]:
        raise NotImplementedError
    
    def insert_record(self, table: str, record: dict[str, Any], commit: bool = False) -> None:
        raise NotImplementedError
    
    def insert_records(self, table: str, records: list[dict[str, Any]], commit: bool = False) -> None:
        raise NotImplementedError
    
    def create_table(self, name: str, columns: dict[str, str], exist_ok: bool = True, commit: bool = False) -> None:
        raise NotImplementedError
    
    def exists(self, table: str) -> bool:
        raise NotImplementedError