from sqlite3 import Connection, Cursor
from typing import Any, Literal, Union
from ..database import RelDatabase
from typing_extensions import TypedDict

class SqliteOptions(TypedDict):
    path: str

class SqliteDatabase(RelDatabase):
    def __init__(self, connection_args: dict = SqliteOptions) -> None:
        super().__init__(connection_args)
        self.connection: Connection = None
        self.cursor: Cursor = None

    def execute(self, query: str, commit: bool = False) -> list[dict[str, Any]]:
        if not self.connection:
            self.connection = Connection(self.connection_args["path"])
        if not self.cursor:
            self.cursor = self.connection.cursor()
        
        result = self.cursor.execute(query)
        description = result.description
        results = result.fetchall()
        if commit:
            self.connection.commit()
            self.cursor.close()
            self.connection.close()
            self.connection = None
            self.cursor = None
        
        return [{description[v][0]: i[v] for v in range(len(i))} for i in results]
    
    def commit(self) -> None:
        if self.connection and self.cursor:
            self.connection.commit()
            self.cursor.close()
            self.connection.close()
            self.connection = None
            self.cursor = None

    def rollback(self) -> None:
        if self.connection and self.cursor:
            self.connection.rollback()
            self.cursor.close()
            self.connection.close()
            self.connection = None
            self.cursor = None

    def get_table(self, table: str, columns: list[str] | Literal['*'] = "*") -> list[dict[str, Any]]:
        columns = ", ".join(columns) if columns != "*" else "*"
        return self.execute("SELECT {cols} FROM {table}".format(
            cols=columns,
            table=table
        ))
    
    def get_columns(self, columns: dict[str, list[str]], primary: str) -> list[dict[str, Any]]:
        column_array = []
        for table, c in columns.items():
            column_array.extend(**[f"{table}.{i}" for i in c])
        
        tables = list(columns.keys())
        
        query = "SELECT {columns} FROM {first_table} {joins};".format(
            columns=column_array,
            first_table=tables[0],
            joins = " ".join(["INNER JOIN {table} ON {last}.{primary} = {table}.{primary}".format(
                table=tables[i],
                last=tables[i-1],
                primary=primary
            ) for i in range(1, len(tables))])
        )
        print(query)
        return self.execute(query)
    
    def exists(self, table: str) -> bool:
        return len(self.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")) > 0
    

