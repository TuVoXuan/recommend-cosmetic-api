from fastapi import APIRouter

from service.comment import get_ratings

comment_router = APIRouter(
    prefix='/comment',
    tags=["Comment"]
)


@comment_router.get('/')
async def getComments():
    return await get_ratings()
