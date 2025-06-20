import pytest
from services.database.connection import db

@pytest.fixture(scope="session", autouse=True)
def close_db_event_loop(request):
    def fin():
        import asyncio
        loop = asyncio.get_event_loop()
        loop.run_until_complete(db.close())
    request.addfinalizer(fin) 