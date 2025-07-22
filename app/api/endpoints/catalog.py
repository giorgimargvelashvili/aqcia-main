from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import session as db_session, models
from app.schemas import product_schemas
from typing import List
from app.schemas.catalog_schemas import CategoryOut, CategoryCreate, CategoryUpdate
from app.db.models import Category

router = APIRouter()

@router.get("/", response_model=List[product_schemas.Product])
def get_catalog(skip: int = 0, limit: int = 100, db: Session = Depends(db_session.get_db)):
    return db.query(models.Product).offset(skip).limit(limit).all()

@router.get("/categories", response_model=List[str])
def get_categories(db: Session = Depends(db_session.get_db)):
    # Get all unique product types (categories)
    categories = db.query(models.Product.type).distinct().all()
    return [c[0] for c in categories if c[0]]

@router.get("/category/{category_name}", response_model=List[product_schemas.Product])
def get_products_by_category(category_name: str, skip: int = 0, limit: int = 100, db: Session = Depends(db_session.get_db)):
    products = db.query(models.Product).filter(models.Product.type == category_name).offset(skip).limit(limit).all()
    if not products:
        raise HTTPException(status_code=404, detail="No products found for this category")
    return products

@router.get("/categories/v2", response_model=List[CategoryOut])
def get_all_categories(db: Session = Depends(db_session.get_db)):
    return db.query(Category).all()

@router.get("/categories/v2/{id}", response_model=CategoryOut)
def get_category(id: int, db: Session = Depends(db_session.get_db)):
    category = db.query(Category).filter(Category.id == id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.post("/categories/v2", response_model=CategoryOut)
def create_category(category: CategoryCreate, db: Session = Depends(db_session.get_db)):
    db_category = Category(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

@router.put("/categories/v2/{id}", response_model=CategoryOut)
def update_category(id: int, category: CategoryUpdate, db: Session = Depends(db_session.get_db)):
    db_category = db.query(Category).filter(Category.id == id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    for field, value in category.dict().items():
        setattr(db_category, field, value)
    db.commit()
    db.refresh(db_category)
    return db_category

@router.delete("/categories/v2/{id}", response_model=dict)
def delete_category(id: int, db: Session = Depends(db_session.get_db)):
    db_category = db.query(Category).filter(Category.id == id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(db_category)
    db.commit()
    return {"detail": "Category deleted"}
