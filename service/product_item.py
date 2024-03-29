from pydantic import BaseModel
from itemBased import ItemBased
from models.product_item import ProductItem, ProdItemTag
from typing import List
from serializer.produc_item import product_items_serializer
from .tag import get_tags, find_tag_weight, find_child_tag
import pandas as pd
from .comment import get_ratings
from .user import get_user_ids
from sklearn.metrics.pairwise import cosine_similarity
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

    rows = [item.id for item in items]
    coloumns = [str(tag.id) for tag in tags]

    df = pd.DataFrame(0, columns=coloumns, index=rows)
    for item in items:
        for tag in item.tags:
            df[tag][item.id] = find_tag_weight(tag, tags)

    result = recommend_item(id, df).to_dict()
    filter_result = [key for key in result if result[key] > 0.3]

    return filter_result


async def recommend_CF_chatbot(user_tags: List[str]):
    items = await get_product_by_category_tag(user_tags[0])
    tags = await get_tags()

    rows = [item.id for item in items]
    coloumns = [str(tag.id) for tag in tags]

    user_profile = []

    for x in coloumns:
        if x in user_tags:
            user_profile.append(1)
        else:
            user_profile.append(0)

    print('user_profile: ', user_profile)
    df = pd.DataFrame(0, columns=coloumns, index=rows)
    for item in items:
        for tag in item.tags:
            df[tag][item.id] = 1

    df.loc['user_profile'] = user_profile

    result = recommend_item('user_profile', df, 10).to_dict()
    filter_result = [key for key in result if result[key] > 0.3]

    return filter_result


def recommend_item(id: str, item_profile: pd.DataFrame, limit=20):
    similarity_matrix = cosine_similarity(item_profile)
    similarity_df = pd.DataFrame(
        similarity_matrix, index=item_profile.index, columns=item_profile.index)
    product_index = similarity_df.index.get_loc(id)

    top = similarity_df.iloc[product_index].sort_values(ascending=False)[
        1:(limit+1)]
    return top


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


async def get_product_by_category_tag(category_tag_id: str):
    products = await ProductItem.find_many({'tags': ObjectId(category_tag_id)}).to_list()

    return product_items_serializer(products)
