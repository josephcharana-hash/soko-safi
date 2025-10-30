#!/usr/bin/env python3
import sqlite3
import os

def clear_products():
    db_path = os.path.join(os.path.dirname(__file__), 'instance', 'soko_safi.db')
    
    if not os.path.exists(db_path):
        print(f"Database not found at {db_path}")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Delete all product images first (foreign key constraint)
        cursor.execute("DELETE FROM product_images")
        images_deleted = cursor.rowcount
        
        # Delete all products
        cursor.execute("DELETE FROM products")
        products_deleted = cursor.rowcount
        
        conn.commit()
        conn.close()
        
        print(f"Successfully deleted {products_deleted} products and {images_deleted} product images")
        
    except Exception as e:
        print(f"Error clearing products: {e}")

if __name__ == "__main__":
    clear_products()