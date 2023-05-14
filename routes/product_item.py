from fastapi import APIRouter
from service.product_item import get_prodItems, recommend_CF, get_product_item_id, recommend_item_based

product_item_router = APIRouter(
    prefix='/product-item',
    tags=["Product Item"]
)


@product_item_router.get('/recommend/{id}')
async def get_similar_product_items(id: str):
    return await recommend_CF(id)


@product_item_router.get('/all-id')
async def get_product_items_id():
    return await get_product_item_id()


@product_item_router.get('/recommend-item-based/{user_id}')
async def get_recommend_item_based(user_id: str):
    return await recommend_item_based(user_id)


@product_item_router.get('/{id}')
async def get_product_items(id: str):
    return await get_prodItems(id)
