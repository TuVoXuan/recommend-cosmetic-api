from models.user import User
from typing import List


async def get_user_ids() -> List[str]:
    result: List[str] = []
    users = await User.find_all().to_list()

    for item in users:
        result.append(str(item.id))

    return result
