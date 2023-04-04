from fastapi import FastAPI
from routes.product_item import product_item_router
from routes.tag import tag_router
from routes.comment import comment_router
from routes.user import user_router
from database import init_db

app = FastAPI()


@app.on_event('startup')
async def connect():
    await init_db()

app.include_router(product_item_router)
app.include_router(tag_router)
app.include_router(comment_router)
app.include_router(user_router)
