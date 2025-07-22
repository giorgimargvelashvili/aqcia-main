import sys
import os
from datetime import datetime, timedelta

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.db.models import Product, Price, Store, Category

def verify_data():
    db: Session = SessionLocal()
    print("--- Verifying Scraper Data ---")
    
    try:
        # 1. Check for the "Agrohub" store
        print("\n[1] Checking for 'Agrohub' store...")
        agrohub_store = db.query(Store).filter(Store.name == "Agrohub").first()
        if agrohub_store:
            print(f"  - SUCCESS: Found store '{agrohub_store.name}' (ID: {agrohub_store.store_id}).")
        else:
            print("  - FAILED: 'Agrohub' store not found.")
            return

        # 2. Check for recently added products
        print("\n[2] Checking for recently added products...")
        recent_products = db.query(Product).order_by(Product.product_id.desc()).limit(5).all()
        if recent_products:
            print(f"  - SUCCESS: Found {len(recent_products)} recent products.")
            for p in recent_products:
                print(f"    - Product: {p.name} (ID: {p.product_id})")
        else:
            print("  - FAILED: No products found in the database.")
            return

        # 3. Check for recent price entries for the Agrohub store
        print("\n[3] Checking for recent price entries from Agrohub...")
        ten_minutes_ago = datetime.utcnow() - timedelta(minutes=10)
        recent_prices = db.query(Price).filter(
            Price.store_id == agrohub_store.store_id,
            Price.updated_at >= ten_minutes_ago
        ).limit(5).all()
        
        if recent_prices:
            print(f"  - SUCCESS: Found {len(recent_prices)} new price entries linked to Agrohub.")
            for price in recent_prices:
                product_name = db.query(Product.name).filter(Product.product_id == price.product_id).scalar()
                print(f"    - Product '{product_name}' has new price: {price.price}")
        else:
            print("  - INFO: No new prices recorded for Agrohub in the last 10 minutes.")
            print("    (This is okay if the scraper hasn't run recently).")

        # 4. Check for categories
        print("\n[4] Checking for categories...")
        categories = db.query(Category).limit(10).all()
        if categories:
            print(f"  - SUCCESS: Found {len(categories)} categories.")
            for c in categories:
                print(f"    - Category: {c.name_en} (ID: {c.id})")
        else:
            print("  - FAILED: No categories found.")

    except Exception as e:
        print(f"\nAn error occurred during verification: {e}")
    finally:
        db.close()
        print("\n--- Verification Complete ---")

if __name__ == "__main__":
    verify_data() 