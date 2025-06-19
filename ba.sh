# 1. Activate venv
source venv/bin/activate

# 2. Check Docker services
docker-compose ps

# 3. Test database connection
python -c "
import asyncio
from services.database.connection import db
async def test(): 
    await db.initialize()
    print('✅ Database connected')
asyncio.run(test())
"
