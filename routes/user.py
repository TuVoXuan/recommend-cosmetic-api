from fastapi import APIRouter

from service.user import get_user_ids

user_router = APIRouter(
    prefix='/user',
    tags=["User"]
)


@user_router.get('/userIds')
async def get_users_id():
    return await get_user_ids()
