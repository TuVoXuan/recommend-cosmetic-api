import motor
import motor.motor_asyncio
import beanie
from models.order_item import OrderItem
from models.product_item import ProductItem
from models.tag_group import TagGroup
from models.variation_option import VariationOption
from models.variation import Variation
from models.tag import Tag
from models.comment import Comment
from models.user import User
from config.config import Settings


async def init_db():
    try:
        client = motor.motor_asyncio.AsyncIOMotorClient(
            Settings().DATABASE_URL)

        await beanie.init_beanie(
            database=client.hygge,
            document_models=[ProductItem, VariationOption,
                             Variation, Tag, TagGroup, Comment, OrderItem, User]
        )
    except:
        print('Cannot connec to database')
