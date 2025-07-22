from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.base import get_db
from app.db.models import CartItem, Product
from app.schemas.cart_schemas import CartItemCreate, CartItem

router = APIRouter()

@router.post("/add")
def add_to_cart():
    return {"message": "Added to cart (placeholder)"}

@router.get("/")
def get_cart():
    return {"cart": []}
