from models.product_item import ProductItem, ProdItemTag
from typing import List
from serializer.produc_item import product_items_serializer
from .tag import get_tags
import pandas as pd

async def get_prodItems() -> List[ProdItemTag]:
    prodItems = await ProductItem.find_all().to_list()
    return product_items_serializer(prodItems)
    # return prodItems


async def recommend_CF(id: str):
    items = await get_prodItems()
    tags = await get_tags()

    coloumns = [item.id for item in items]
    rows = [str(tag.id) for tag in tags]

    df = pd.DataFrame(0, columns=coloumns, index=rows)
    for item in items:
        for tag in item.tags:
            df[item.id][tag] = 1

    result = recommend_item(id, df)

    return result


def recommend_item(id: str, item_profile: pd.DataFrame):
    item = item_profile[id]
    similar_item = item_profile.corrwith(item)
    similar_item = similar_item.sort_values(ascending=False)
    similar_item = similar_item.iloc[1:]
    return similar_item.head(20)