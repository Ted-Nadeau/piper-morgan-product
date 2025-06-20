import pytest
import sys
import os
from services.database.connection import db

# Add project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

@pytest.fixture(scope="session", autouse=True)
def close_db_event_loop(request):
    def fin():
        import asyncio
        loop = asyncio.get_event_loop()
        loop.run_until_complete(db.close())
    request.addfinalizer(fin) 