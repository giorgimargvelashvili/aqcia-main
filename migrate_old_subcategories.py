import sys
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.db.models import Category, Subcategory, Product

def migrate_old_subcategories():
    db: Session = SessionLocal()
    try:
        # Step 1: Find all category names that are already used as subcategories
        subcat_names = set([s.name for s in db.query(Subcategory).all()])
        cat_names = set([c.name for c in db.query(Category).all()])

        # Step 2: Find categories that are not true categories (i.e., likely old subcategories)
        # We'll consider as old subcategories any category whose name is also present in subcategories
        # and is not referenced as a parent by any subcategory
        old_subcats = db.query(Category).filter(Category.name.in_(subcat_names)).all()

        print(f"Found {len(old_subcats)} old subcategories to migrate.")

        for old_cat in old_subcats:
            # Try to find the parent category by matching the new subcategory's category_id
            new_subcat = db.query(Subcategory).filter(Subcategory.name == old_cat.name).first()
            if new_subcat:
                parent_category_id = new_subcat.category_id
            else:
                # Fallback: assign to a generic category (first one)
                parent_category = db.query(Category).first()
                parent_category_id = parent_category.id if parent_category else None

            # Create the subcategory if it doesn't exist
            if not new_subcat:
                new_subcat = Subcategory(
                    name=old_cat.name,
                    name_ka=getattr(old_cat, 'name_ka', None),
                    name_en=getattr(old_cat, 'name_en', None),
                    name_ru=getattr(old_cat, 'name_ru', None),
                    icon=getattr(old_cat, 'icon', None),
                    api_subcategory_id=None,
                    category_id=parent_category_id
                )
                db.add(new_subcat)
                db.commit()
                db.refresh(new_subcat)

            # Update products that referenced the old category
            products = db.query(Product).filter(Product.subcategory_id == None).all()
            for product in products:
                # If the product's name matches the subcategory, link it
                if product.name and product.name in subcat_names:
                    product.subcategory_id = new_subcat.id
            db.commit()

            # Delete the old category row
            db.delete(old_cat)
            db.commit()

        print("Migration complete. Old subcategories moved and cleaned up.")
    except Exception as e:
        print(f"Error during migration: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    migrate_old_subcategories() 