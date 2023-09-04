from typing import Any
from typing_extensions import TypedDict

from ..base import AbstractDatabase, TableColumn
import sqlite3


class SqliteOptions(TypedDict):
    path: str


class SqliteDatabase(AbstractDatabase):
    def __init__(self, connection_options: SqliteOptions = {}) -> None:
        self.connection: sqlite3.Connection
        super().__init__(connection_options)

    def connect(self, options: SqliteOptions) -> sqlite3.Connection:
        return sqlite3.connect(options["path"])
    
    def query(self, query: str) -> list[dict]:
        cur = self.connection.cursor()
        result = cur.execute(query)
        return [{d[0]: v for d, v in zip(result.description, i)} for i in result.fetchall()]
    
    def exists(self, table: str) -> bool:
        return len(self.query(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}';")) > 0
    
    def create_table(self, name: str, columns: list[tuple[str, str]] = [], if_exists: str = "ignore"):
        if self.exists(name):
            if if_exists == "error":
                raise sqlite3.OperationalError
            return
        
        self.query("CREATE TABLE {name} ({columns})".format(
            name=name,
            columns=", ".join([c[0] + " " + c[1] if len(c) == 2 else c[0] for c in columns])
        ))

    def info(self, table: str) -> list[TableColumn]:
        columns = self.query(f"PRAGMA table_info({table});")
        return [TableColumn(
            index=col["cid"],
            name=col["name"],
            type=col["type"],
            not_null=bool(col["notnull"]),
            default_value=col["dflt_value"],
            primary_key=bool(col["pk"])
        ) for col in sorted(columns, key=lambda c: c["cid"])]
    
    def insert(self, table: str, data: dict[str, Any]):
        table_info = self.info(table)
        values = ["'" + data[i["name"]] + "'" if type(data[i["name"]]) == str else str(data[i["name"]]) if i["name"] in data.keys() else i["default_value"] for i in table_info]
        self.query("INSERT INTO {table} ({columns}) VALUES({values});".format(
            table=table,
            columns=", ".join([c["name"] for c in table_info]),
            values=", ".join(values)
        ))
        self.connection.commit()
        self.connection.close()
        self.connection = sqlite3.Connection(self.connection_options["path"])

    
