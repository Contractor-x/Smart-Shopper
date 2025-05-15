from fastapi import APIRouter, Body
from app.services.mcp_client import extract_product_data

router = APIRouter()

@router.post("/scrape")
async def scrape_products(urls: list[str] = Body(...)):
    return await extract_product_data(urls)
