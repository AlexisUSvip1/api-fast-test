from app.core.database import AsyncSessionLocal

async def get_context():
    async with AsyncSessionLocal() as db:
        yield {"db": db}
