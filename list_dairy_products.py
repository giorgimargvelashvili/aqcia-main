import sys
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.db.models import Product, Category, Subcategory

CATEGORY_NAME = "რძის პროდუქტები, კვერცხი, ყველი"

def list_dairy_products():
    db: Session = SessionLocal()
    try:
        # Find the category by name (Georgian)
        category = db.query(Category).filter(Category.name == CATEGORY_NAME).first()
        if not category:
            print(f"Category '{CATEGORY_NAME}' not found.")
            return
        print(f"Category: {category.name} (ID: {category.id})\n")

        # Find all subcategories under this category
        subcategories = db.query(Subcategory).filter(Subcategory.category_id == category.id).all()
        subcat_ids = [s.id for s in subcategories]
        subcat_map = {s.id: s.name for s in subcategories}

        # Find all products in these subcategories
        products = db.query(Product).filter(Product.subcategory_id.in_(subcat_ids)).all()
        if not products:
            print("No products found in this category.")
            return

        print(f"Products in '{CATEGORY_NAME}':\n")
        for product in products:
            subcat_name = subcat_map.get(product.subcategory_id, "Unknown")
            print(f"- Product: {product.name} (ID: {product.product_id}), Subcategory: {subcat_name}")
    finally:
        db.close()

if __name__ == "__main__":
    list_dairy_products() 