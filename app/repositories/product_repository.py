from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from app.models.product_model import Product

class ProductRepository:
    @staticmethod
    async def get_all(db: AsyncSession, search: str | None = None, offset: int = 0, limit: int = 20) -> dict:
        # Base query for products
        query = select(Product)
        # Base query for count
        count_query = select(func.count(Product.id))

        if search:
            filter_cond = (
                Product.name.ilike(f"%{search}%") | 
                Product.description.ilike(f"%{search}%")
            )
            query = query.where(filter_cond)
            count_query = count_query.where(filter_cond)

        # Get total count
        total_products = await db.scalar(count_query)

        # Get paginated products
        query = query.offset(offset).limit(limit)
        result = await db.execute(query)
        
        return {
            "total": total_products or 0,
            "products": list(result.scalars().all())
        }

    @staticmethod
    async def get_by_id(db: AsyncSession, product_id: UUID) -> Product | None:
        query = select(Product).where(Product.id == product_id)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    @staticmethod
    async def create(db: AsyncSession, product: Product) -> Product:
        db.add(product)
        await db.commit()
        await db.refresh(product)
        return product

    @staticmethod
    async def update(db: AsyncSession, product: Product) -> Product:
        await db.commit()
        await db.refresh(product)
        return product

    @staticmethod
    async def delete(db: AsyncSession, product: Product) -> None:
        await db.delete(product)
        await db.commit()
