#!/usr/bin/env python3
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.models import db, Product, ProductImage
from app import create_app

def delete_all_products():
    app = create_app()
    with app.app_context():
        try:
            # Delete all product images first
            ProductImage.query.delete()
            
            # Delete all products
            Product.query.delete()
            
            db.session.commit()
            print("All products and images deleted successfully!")
            
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting products: {e}")

if __name__ == "__main__":
    delete_all_products()