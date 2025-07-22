from fastapi import APIRouter, Depends, HTTPException, Header
from typing import List
from app.schemas.data_collection_schemas import ProductData
from app.services.data_collection import process_scraped_data

router = APIRouter()

API_KEY = "supersecretapikey"  # Change this to something secure and share with your coworker

def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

@router.post("/upload", dependencies=[Depends(verify_api_key)])
async def upload_scraped_data(data: List[ProductData]):
    process_scraped_data(data)
    return {"status": "success"} 