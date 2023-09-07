from pythrel.adapters.sqlite import SqliteDatabase
import secrets
import random
import os

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

    print(db.query().select("customers", ["customerName", "favorite_number", "quantity"]).join("products", "inner", "customers.id = products.customer").where("products.quantity > 40").order("quantity").execute())