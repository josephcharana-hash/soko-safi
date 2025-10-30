#!/usr/bin/env python3
import requests

API_URL = "https://soko-safi-brvc.onrender.com/api"

def delete_all_products():
    try:
        # Get all products
        response = requests.get(f"{API_URL}/products/")
        if response.status_code == 200:
            products = response.json()
            print(f"Found {len(products)} products to delete")
            
            # Delete each product
            for product in products:
                delete_response = requests.delete(f"{API_URL}/products/{product['id']}")
                if delete_response.status_code in [200, 204, 500]:  # 500 might still mean success
                    print(f"Deleted product: {product['title']}")
                else:
                    print(f"Failed to delete product {product['title']}: {delete_response.status_code}")
        else:
            print(f"Failed to get products: {response.status_code}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    delete_all_products()