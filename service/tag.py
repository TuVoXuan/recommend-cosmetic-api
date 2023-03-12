from models.tag import Tag
from typing import List

async def get_tags() -> List[Tag]:
    tags = await Tag.find_all().to_list()
    return tags

def find_tag_weight(tag_id:str ,tags: List[Tag]) -> int:
    for tag in tags:
        if str(tag.id) == tag_id:
            return tag.weight