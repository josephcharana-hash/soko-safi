from app import app
from app.models import db, User, Product, Category, UserRole
from faker import Faker
import random

fake = Faker()

def seed_database():
    with app.app_context():
        # Create categories first
        categories = []
        for i in range(10):
            category = Category(
                name=fake.word().capitalize(),
                description=fake.sentence()
            )
            db.session.add(category)
            categories.append(category)
        
        db.session.commit()
        
        # Create 100 users
        users = []
        for i in range(100):
            user = User(
                role=random.choice([UserRole.buyer, UserRole.artisan]),
                email=fake.unique.email(),
                password_hash=fake.password(),
                full_name=fake.name(),
                phone=fake.phone_number()[:30],
                location=fake.city()
            )
            db.session.add(user)
            users.append(user)
        
        db.session.commit()
        
        # Create 100 products
        artisans = [u for u in users if u.role == UserRole.artisan]
        for i in range(100):
            product = Product(
                artisan_id=random.choice(artisans).id if artisans else users[0].id,
                category_id=random.choice(categories).id,
                title=fake.catch_phrase(),
                description=fake.text(max_nb_chars=200),
                price=round(random.uniform(10.0, 500.0), 2),
                currency='USD',
                stock=random.randint(1, 50)
            )
            db.session.add(product)
        
        db.session.commit()
        print("Database seeded with 100 users and 100 products!")

if __name__ == '__main__':
    seed_database()