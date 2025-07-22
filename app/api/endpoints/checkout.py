from fastapi import APIRouter

router = APIRouter()

@router.post("/")
def checkout():
    return {"message": "Checkout successful (placeholder)"}
