# Test if patterns are handled
python3 -c "
from services.intent_service import classifier
import asyncio

test_patterns = [
    'create an issue about login bug',  # CREATE action
    'update issue status',              # UPDATE action
    'search for architecture docs',     # SEARCH action
]

async def test():
    for pattern in test_patterns:
        result = await classifier.classify(pattern)
        print(f'{pattern} -> {result.get(\"category\", \"UNKNOWN\")}')

asyncio.run(test())
"
