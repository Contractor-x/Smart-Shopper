from fastapi import APIRouter, Body
from app.services.llm_agent import analyze_products

router = APIRouter()

@router.post("/analyze")
async def analyze(products: list[dict] = Body(...)):
    return analyze_products(products)
