# Install
brew install git-secrets

# Navigate to your repo
cd ~/Development/piper-morgan

# Initialize git-secrets for this repo
git secrets --install

# Add common AWS patterns (useful baseline)
git secrets --register-aws

# Add Google API key pattern
git secrets --add 'AIza[0-9A-Za-z_-]{35}'

# Add other common patterns
git secrets --add 'sk-[0-9a-zA-Z]{48}'          # OpenAI
git secrets --add 'ghp_[0-9a-zA-Z]{36}'         # GitHub PAT
git secrets --add 'xoxb-[0-9a-zA-Z-]+'          # Slack bot token
git secrets --add 'xoxp-[0-9a-zA-Z-]+'          # Slack user token

# Scan your history to verify (optional but recommended)
git secrets --scan-history
