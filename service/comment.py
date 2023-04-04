from typing import List
from models.comment import Comment, OutputComment
from serializer.comment import comments_serializer


async def get_ratings() -> List[OutputComment]:
    ratings = await Comment.aggregate([
        {
            "$lookup": {
                "from": 'orderitems',
                "localField": "orderItem",
                "foreignField": '_id',
                "as": "orderItem",
                "pipeline": [
                    {
                        "$project": {
                            "productItem": 1
                        }
                    }
                ]
            }
        },
        {
            '$addFields': {
                'productItem': "$orderItem.productItem"
            }
        },
        {
            "$group": {
                "_id": {
                    "user": "$user",
                    "productItem": "$productItem"
                },
                "avgRate": {"$avg": "$rate"}
            }
        },
        {"$replaceRoot": {"newRoot": {"$mergeObjects":  ['$_id', "$$ROOT"]}}},
        {
            "$project": {
                "user": 1,
                "avgRate": 1,
                "productItem": 1
            }
        }
    ]).to_list()

    print(ratings[0])
    return comments_serializer(ratings)
