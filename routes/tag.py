from fastapi import APIRouter
from service.tag import get_tags

tag_router = APIRouter(
    prefix='/tag',
    tags=["Tag"]
)

@tag_router.get('/')
async def getTags():
    return await get_tags()