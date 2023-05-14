from pydantic import BaseModel
from itemBased import ItemBased
from models.product_item import ProductItem, ProdItemTag
from typing import List
from serializer.produc_item import product_items_serializer
from .tag import get_tags, find_tag_weight, find_child_tag
import pandas as pd
from .comment import get_ratings
from .user import get_user_ids
from bson import ObjectId


async def get_prodItems(prodId: str) -> List[ProdItemTag]:
    tags = await find_child_tag()
    pipeline = [
        {"$match": {"_id": ObjectId(prodId)}},
        {"$lookup": {
            "from": "tags",
            "localField": "tags",
            "foreignField": "_id",
            "as": "tags"
        }},
        {"$unwind": "$tags"},
        {"$replaceRoot": {"newRoot": "$tags"}}
    ]

    productTags = await ProductItem.aggregate(pipeline).to_list()

    prodTagIds = [str(tag['_id']) for tag in productTags]

    commonTags = [ObjectId(tag) for tag in prodTagIds if tag in tags]

    prodItems = await ProductItem.find_many({'tags': {'$in': commonTags}}).to_list()
    return product_items_serializer(prodItems)


async def recommend_CF(id: str):
    items = await get_prodItems(id)
    tags = await get_tags()

    coloumns = [item.id for item in items]
    rows = [str(tag.id) for tag in tags]

    df = pd.DataFrame(0, columns=coloumns, index=rows)
    for item in items:
        for tag in item.tags:
            df[item.id][tag] = find_tag_weight(tag, tags)

    result = recommend_item(id, df).to_dict()
    filter_result = [key for key in result if result[key] > 0.3]

    return filter_result


def recommend_item(id: str, item_profile: pd.DataFrame):
    item = item_profile[id]
    similar_item = item_profile.corrwith(item)
    similar_item = similar_item.sort_values(ascending=False)
    similar_item = similar_item.iloc[1:]

    return similar_item.head(20)


async def get_product_item_id():
    result: List[str] = []
    prodItems = await ProductItem.find_all().to_list()

    for item in prodItems:
        result.append(str(item.id))

    return result


async def recommend_item_based(user_id: str):
    result: List[str] = []
    ratings = await get_ratings()

    df = pd.DataFrame.from_dict([e.to_dict() for e in ratings])

    item_based_filtering = ItemBased(df)
    recommend_product_item = item_based_filtering.predict(
        picked_userid=user_id, number_of_recommendations=10, number_of_similar_items=5)

    for item in recommend_product_item:
        result.append(item[0])
    return result
