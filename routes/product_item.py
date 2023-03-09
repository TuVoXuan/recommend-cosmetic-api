from fastapi import APIRouter
from service.product_item import get_prodItems, recommend_CF

product_item_router = APIRouter(
    prefix='/product-item',
    tags=["Product Item"]
)

@product_item_router.get('/recommend/{id}')
async def get_similar_product_items(id: str):
    return await recommend_CF(id)

@product_item_router.get('/')
async def get_product_items():
    return await get_prodItems()


