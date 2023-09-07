from pythrel import SqliteDatabase, Pythrel, Record
import secrets
import random
import os

class Customer(Record):
    id: int
    customerName: str
    favorite_number: float

def main():
    try:
        os.remove("test.db")
    except:
        pass
    db = SqliteDatabase({"path": "test.db"})
    db.create_table("customers", {"id": "INTEGER", "customerName": "TEXT", "favorite_number": "REAL"})
    db.create_table("products", {"id": "INTEGER", "customer": "INTEGER", "productName": "TEXT", "quantity": "INTEGER"})
    db.commit()

    CUSTOMERS = {}
    for c in range(500):
        CUSTOMERS[c] = {
            "id": c,
            "customerName": secrets.token_urlsafe(8),
            "favorite_number": random.randint(0, 10000)
        }

    PRODUCTS = {}
    for c in range(1000):
        PRODUCTS[c] = {
            "id": c,
            "customer": random.randint(0, len(CUSTOMERS.keys()) - 1),
            "productName": "PROD-" + secrets.token_urlsafe(8),
            "quantity": random.randint(0, 50)
        }
    
    db.query().insert("customers", list(CUSTOMERS.values())).execute()
    db.query().insert("products", list(PRODUCTS.values())).execute()
    db.commit()

    orm = Pythrel(db)
    print(orm.load_columns(Customer, "customers", "*")[0].dict())
    orm.create(Customer, "customers", id=-10, customerName="John", favorite_number=-69)
    john = orm.load_columns(Customer, "customers", "*", where="id < 0")[0]
    print(john)
    john.favorite_number = 1000
    orm.save(john, key="id")
    print(orm.load_query(Customer, orm.query().select("customers", "*").where("id < 0"))[0])