# Check how Piper loads environment
python -c "
from services.configuration.piper_config_loader import PiperConfigLoader
import os

print('=== Piper Config Environment Check ===')
loader = PiperConfigLoader()

# Check if Piper has GitHub token
token = os.getenv('GITHUB_TOKEN')
print(f'GITHUB_TOKEN in environment: {token is not None}')
if token:
    print(f'Token length: {len(token)}')
    print(f'Token format: {token[:4]}...')
"
