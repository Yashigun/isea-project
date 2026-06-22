from sqlalchemy import text
from app.db.database import engine
import asyncio


async def test_connection():
    async with engine.connect() as conn:
        result = await conn.execute(text("SELECT 1"))
        print(result.scalar())


if __name__ == "__main__":
    asyncio.run(test_connection())