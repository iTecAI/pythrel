from pythrel.adapters.sqlite import SqliteDatabase
import secrets

def main():
    db = SqliteDatabase({"path": "test.db"})
    db.create_table("customers", [
        ("name", ),
        ("birthday", ),
        ("baby", )
    ])
    print(db.info("customers"))
    db.insert("customers", {"name": secrets.token_urlsafe(8), "birthday": 0, "baby": 0})
    print(db.query("SELECT * FROM customers"))