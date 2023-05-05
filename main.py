from fastapi import FastAPI
from routes.product_item import product_item_router
from routes.tag import tag_router
from routes.comment import comment_router
from routes.user import user_router
from routes.translation import traslation_router
from database import init_db
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
def read_root():
    return 'This is api for cosmetic shop'


@app.on_event('startup')
async def connect():
    await init_db()

app.include_router(product_item_router)
app.include_router(tag_router)
app.include_router(comment_router)
app.include_router(user_router)
app.include_router(traslation_router)
