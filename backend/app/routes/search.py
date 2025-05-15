from fastapi import APIRouter, Query
from app.services.mcp_client import discover_products

router = APIRouter()

@router.get("/search")
async def search_products(q: str = Query(..., alias="query")):
    return await discover_products(q)
