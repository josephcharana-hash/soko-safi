from server.models import db, User, Product
from server.run import app

with app.app_context():
    # Clear existing data
    db.session.query(User).delete()
    db.session.query(Product).delete()

    # Add sample users
    user1 = User(username="Queentel", email="queentel@example.com", password="12345")
    user2 = User(username="JohnDoe", email="john@example.com", password="secret")

    # Add sample products
    product1 = Product(name="Organic Soap", price=5.99, description="Natural handmade soap")
    product2 = Product(name="Lotion", price=8.50, description="Smooth moisturizing lotion")

    db.session.add_all([user1, user2, product1, product2])
    db.session.commit()

    print("✅ Database seeded successfully!")
