# Claude Code Session Logging Aliases
# Add these to your ~/.zshrc or ~/.bashrc

# Automatic tee logging for terminal Claude Code sessions
alias cc-prog='claude | tee ~/Development/piper-morgan/dev/archive/$(date +%Y/%m/%d)/$(date +%Y-%m-%d-%H%M)-prog-code-raw.txt'
alias cc-prog-c='claude -c | tee ~/Development/piper-morgan/dev/archive/$(date +%Y/%m/%d)/$(date +%Y-%m-%d-%H%M)-prog-code-raw.txt'
alias cc-prog-skip='claude --dangerously-skip-permissions | tee ~/Development/piper-morgan/dev/archive/$(date +%Y/%m/%d)/$(date +%Y-%m-%d-%H%M)-prog-code-raw.txt'
alias cc-prog-c-skip='claude -c --dangerously-skip-permissions | tee ~/Development/piper-morgan/dev/archive/$(date +%Y/%m/%d)/$(date +%Y-%m-%d-%H%M)-prog-code-raw.txt'
alias cc-prog-r='claude --resume | tee ~/Development/piper-morgan/dev/archive/$(date +%Y/%m/%d)/$(date +%Y-%m-%d-%H%M)-prog-code-raw.txt'
alias cc-prog-r-skip='claude --resume --dangerously-skip-permissions | tee ~/Development/piper-morgan/dev/archive/$(date +%Y/%m/%d)/$(date +%Y-%m-%d-%H%M)-prog-code-raw.txt'

# Alternative: If you want logs in current directory
alias cc-here='claude | tee ./$(date +%Y-%m-%d-%H%M)-prog-code-raw.txt'

# Quick check of today's raw logs
alias cc-logs='ls -lah ~/Development/piper-morgan/dev/archive/$(date +%Y/%m/%d)/'

# Read the last raw session log
alias cc-last='tail -n 100 $(ls -t ~/Development/piper-morgan/dev/archive/$(date +%Y/%m/%d)/*.txt | head -1)'

# How to use:
# 1. Instead of `claude`, type `cc-prog` to start session with auto-logging
# 2. Instead of `claude -c`, type `cc-prog-c`
# 3. Instead of `claude --dangerously-skip-permissions`, type `cc-prog-skip`
# 4. Instead of `claude -c --dangerously-skip-permissions`, type `cc-prog-c-skip`
# 5. Instead of `claude --resume`, type `cc-prog-r`
# 6. Instead of `claude --resume --dangerously-skip-permissions`, type `cc-prog-r-skip`
# 7. Everything gets captured to dev/archive/YYYY/MM/DD/YYYY-MM-DD-HHMM-prog-code-raw.txt
# 8. At end of session, ask Claude to create summary log in dev/active/ if needed
# 9. Review raw logs anytime with `cc-logs` or `cc-last`

# Note: Make sure dev/archive/YYYY/MM/DD directories exist first:
# mkdir -p ~/Development/piper-morgan/dev/archive/$(date +%Y/%m/%d)
