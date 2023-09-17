from pythrel import PostgresDatabase, Pythrel, Record
import secrets
import random
import os
from dotenv import load_dotenv

load_dotenv()

class Customer(Record):
    id: int
    customer_name: str
    favorite_number: float

def main():
    db = PostgresDatabase(host=os.getenv("HOST"), port=os.getenv("PORT", "5432"), username=os.getenv("USERNAME"), password=os.getenv("PASSWORD"), database=os.getenv("DATABASE"))
    db.create_table("customers", {"id": "integer", "customer_name": "text", "favorite_number": "numeric"})
    db.create_table("products", {"id": "integer", "customer": "integer", "product_name": "text", "quantity": "integer"})
    db.commit()

    CUSTOMERS = {}
    for c in range(20):
        CUSTOMERS[c] = {
            "id": c,
            "customer_name": secrets.token_urlsafe(8),
            "favorite_number": random.randint(0, 10000)
        }

    PRODUCTS = {}
    for c in range(50):
        PRODUCTS[c] = {
            "id": c,
            "customer": random.randint(0, len(CUSTOMERS.keys()) - 1),
            "product_name": "PROD-" + secrets.token_urlsafe(8),
            "quantity": random.randint(0, 50)
        }
    
    db.query().insert("customers", list(CUSTOMERS.values())).execute()
    db.query().insert("products", list(PRODUCTS.values())).execute()
    db.commit()

    orm = Pythrel(db)
    print(orm.load_columns(Customer, "customers", "*")[0].model_dump())
    orm.create(Customer, "customers", id=-10, customer_name="John", favorite_number=-69)
    john = orm.load_columns(Customer, "customers", "*", where="id < 0")[0]
    print(john)
    john.favorite_number = 1000
    orm.save(john, key="id")
    print(orm.load_query(Customer, orm.query().select("customers", "*").where("id < 0"))[0])