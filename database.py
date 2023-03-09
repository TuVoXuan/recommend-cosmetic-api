import motor
import motor.motor_asyncio
import beanie
from models.product_item import ProductItem
from models.variation_option import VariationOption
from models.variation import Variation
from models.tag import Tag
from config.config import Settings

async def init_db():
    client = motor.motor_asyncio.AsyncIOMotorClient(Settings().DATABASE_URL)

    await beanie.init_beanie(
        database=client.hygge,
        document_models=[ProductItem, VariationOption, Variation, Tag]
    )