from pythrel.adapters.sqlite import SqliteDatabase
import secrets

def main():
    db = SqliteDatabase({"path": "test.db"})
    result = db.get_table("customers", ["name", "birthday"])
    print(result)