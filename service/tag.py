from models.tag import Tag
from typing import List
from bson import ObjectId


async def get_tags() -> List[Tag]:
    tags = await Tag.find_all().to_list()
    return tags


def find_tag_weight(tag_id: str, tags: List[Tag]) -> int:
    for tag in tags:
        if str(tag.id) == tag_id:
            return tag.weight


async def find_child_tag() -> List[str]:
    childTags = await Tag.find({'parent': ObjectId('6423911e4d6e2f4a34e82d56')}).to_list()
    return [str(tag.id) for tag in childTags]
