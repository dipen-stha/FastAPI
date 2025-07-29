import random

from sqlmodel import select

from app.db.models import Category, Product
from app.db.session import get_db


def seed_categories_and_product_seeder():
    initial_categories = [
        "Laptop",
        "Keyboard",
        "Monitor",
        "Mouse",
        "Accessories",
    ]
    number_of_categories = int(input("Enter the number of categories to create: "))
    number_of_products = int(input("Enter the number of products to create: "))

    db = next(get_db())

    categories = [
        Category(name=f"{random.choices(initial_categories)}")
        for _ in range(number_of_categories)
    ]

    db.add_all(categories)
    db.commit()

    categories = db.exec(select(Category)).all()

    products = [
        Product(
            name=f"Product {i}",
            price=f"{random.randrange(100, 5000, 5)}",
            categories=random.sample(categories, random.randint(1, 5)),
        )
        for i in range(number_of_products)
    ]
    db.add_all(products)
    db.commit()

    return


if __name__ == "__main__":
    seed_categories_and_product_seeder()
