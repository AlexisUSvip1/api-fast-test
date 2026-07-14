from uuid import UUID
import strawberry

@strawberry.type
class ProductType:
    id: UUID
    name: str
    description: str
    price: float
    images_products: list[str]


@strawberry.type
class PaginatedProductType:
    total: int
    products: list[ProductType]

