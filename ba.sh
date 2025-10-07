# 1. How are canonical queries currently passing tests?
python3 -c "
import asyncio
from services.intent_service import IntentService
intent = 'What is my priority today?'  # PRIORITY canonical
result = await IntentService().process_intent(intent, 'test-session')
print(f'Result: {result}')
print(f'Does it error? Does it return something?')
"

# 2. Is there another routing path we're missing?
grep -r "TEMPORAL\|STATUS\|PRIORITY" services/ --include="*.py" | grep -v "test"

# 3. Are canonical handlers being called from somewhere else?
grep -r "canonical_handlers" services/ --include="*.py"
