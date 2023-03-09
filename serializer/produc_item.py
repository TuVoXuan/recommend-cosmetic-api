from models.product_item import ProdItemTag, ProductItem
from typing import List

def product_item_serializer(product_item: ProductItem) -> ProdItemTag:
    return ProdItemTag(
        str(product_item.id),
        [str(tag.to_dict()['id']) for tag in product_item.tags]
    )


def product_items_serializer(product_items: List[ProductItem]) -> List[ProdItemTag]:
    return [product_item_serializer(item) for item in product_items]