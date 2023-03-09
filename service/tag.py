from models.tag import Tag
from typing import List

async def get_tags() -> List[Tag]:
    tags = await Tag.find_all().to_list()
    return tags