from typing import List
from fastapi import APIRouter
from service.translate import translate_to_english
from common import Comment


traslation_router = APIRouter(
    prefix='/translation',
    tags=["Translation"]
)

@traslation_router.post('')
async def translateToEnglish(body: List[Comment]):
    return translate_to_english(body)