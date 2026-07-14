from uuid import UUID
from app.services.product_services import ProductService
from app.models.product_model import Product
from app.api.graphql.types import ProductType, PaginatedProductType
import strawberry

@strawberry.type
class Query:
    @strawberry.field
    async def product(self, info: strawberry.Info, search: str | None = None, offset: int = 0, limit: int = 20) -> PaginatedProductType:
        db = info.context["db"]
        res = await ProductService.get_products(db, search=search, offset=offset, limit=limit)
        return PaginatedProductType(
            total=res["total"],
            products=[
                ProductType(
                    id=p.id,
                    name=p.name,
                    description=p.description,
                    price=p.price,
                    images_products=p.images_products
                ) for p in res["products"]
            ]
        )

    @strawberry.field
    async def get_product_by_id(self, info: strawberry.Info, id: UUID) -> ProductType | None:
        db = info.context["db"]
        return await ProductService.get_product_by_id(db, id)