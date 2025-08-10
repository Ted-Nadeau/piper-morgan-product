import asyncio

from sqlalchemy import select

from services.database.connection import db
from services.database.models import UploadedFileDB


async def check_files():
    await db.initialize()
    async with await db.get_session() as session:
        result = await session.execute(
            select(
                UploadedFileDB.session_id,
                UploadedFileDB.filename,
                UploadedFileDB.upload_time,
            )
            .order_by(UploadedFileDB.upload_time.desc())
            .limit(5)
        )
        files = result.fetchall()
        print(f"Files found: {len(files)}")
        for file in files:
            print(f"Session: {file[0]}, File: {file[1]}, Time: {file[2]}")
    await db.close()


if __name__ == "__main__":
    asyncio.run(check_files())
