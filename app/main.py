from app.api import graphql
from contextlib import asynccontextmanager

from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from app.api.graphql.schema import schema
from app.api.graphql.context import get_context
from app.api.routers import product, auth
from app.core.database import engine, Base
from app.models.product_model import Product
from app.models.user_model import User


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Crea las tablas en la base de datos si no existen
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(title="User store", lifespan=lifespan)
graphql_app = GraphQLRouter(schema, context_getter=get_context)

app.include_router(
    graphql_app,
    prefix="/graphql"
)
app.include_router(product.router_product)
app.include_router(auth.router)