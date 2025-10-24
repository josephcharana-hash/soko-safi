from app.models import db, User, Product
from run import app
import random

with app.app_context():
    # Clear existing data
    db.session.query(User).delete()
    db.session.query(Product).delete()

    # Create 100 users
    users = []
    for i in range(1, 101):
        user = User(
            username=f"user{i}",
            email=f"user{i}@example.com",
            password=f"password{i}"
        )
        users.append(user)

    # Create 100 products
    products = []
    product_names = ["Soap", "Lotion", "Shampoo", "Conditioner", "Cream", "Oil", "Serum", "Mask", "Scrub", "Toner"]
    adjectives = ["Organic", "Natural", "Premium", "Luxury", "Fresh", "Pure", "Gentle", "Moisturizing", "Nourishing", "Revitalizing"]
    
    for i in range(1, 101):
        name = f"{random.choice(adjectives)} {random.choice(product_names)} {i}"
        price = round(random.uniform(5.0, 50.0), 2)
        description = f"High quality {name.lower()} for daily use"
        
        product = Product(name=name, price=price, description=description)
        products.append(product)

    # Add all to database
    db.session.add_all(users + products)
    db.session.commit()

    print("✅ Database seeded with 100 users and 100 products!")