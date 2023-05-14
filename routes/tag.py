from fastapi import APIRouter
from service.tag import get_tags, find_child_tag

tag_router = APIRouter(
    prefix='/tag',
    tags=["Tag"]
)


@tag_router.get('/')
async def getTags():
    return await get_tags()


@tag_router.get('/child-tag')
async def get_child_tags():
    return await find_child_tag()
