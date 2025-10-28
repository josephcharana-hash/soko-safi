#!/usr/bin/env python3
from app import create_app
from app.models import db, Category, User, UserRole, Product
from app.auth import hash_password

def init_database():
    app = create_app()
    
    with app.app_context():
        # Create all tables
        db.create_all()
        print("Database tables created")
        
        # Create categories if they don't exist
        if not Category.query.first():
            categories = [
                Category(name='Pottery', description='Handmade ceramic items'),
                Category(name='Textiles', description='Woven fabrics and clothing'),
                Category(name='Wood Crafts', description='Carved wooden items'),
                Category(name='Jewelry', description='Handcrafted jewelry'),
                Category(name='Baskets', description='Woven baskets and containers'),
                Category(name='Metalwork', description='Metal crafts and tools')
            ]
            
            for category in categories:
                db.session.add(category)
            
            db.session.commit()
            print(f"Created {len(categories)} categories")
        
        # Create sample users if they don't exist
        if not User.query.first():
            users = [
                User(
                    email='artisan@test.com',
                    password_hash=hash_password('password123'),
                    full_name='Test Artisan',
                    role=UserRole.artisan,
                    phone='+254700000001',
                    location='Nairobi',
                    description='Skilled pottery artisan',
                    is_verified=True
                ),
                User(
                    email='buyer@test.com',
                    password_hash=hash_password('password123'),
                    full_name='Test Buyer',
                    role=UserRole.buyer,
                    phone='+254700000002',
                    location='Eldoret',
                    is_verified=True
                )
            ]
            
            for user in users:
                db.session.add(user)
            
            db.session.commit()
            print(f"Created {len(users)} test users")
            
            # Create sample products
            artisan = User.query.filter_by(email='artisan@test.com').first()
            if artisan:
                products = [
                    Product(
                        artisan_id=artisan.id,
                        title='Handcrafted Ceramic Vase',
                        description='Beautiful ceramic vase with traditional patterns',
                        price=2500.00,
                        stock=5,
                        currency='KSh'
                    ),
                    Product(
                        artisan_id=artisan.id,
                        title='Woven Basket Set',
                        description='Set of 3 traditional woven baskets',
                        price=1800.00,
                        stock=3,
                        currency='KSh'
                    )
                ]
                
                for product in products:
                    db.session.add(product)
                
                db.session.commit()
                print(f"Created {len(products)} sample products")

if __name__ == "__main__":
    init_database()