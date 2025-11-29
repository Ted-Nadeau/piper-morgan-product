#!/bin/bash
# Fix the Claude Code aliases in ~/.zshrc

echo "🔧 Fixing Claude Code aliases..."

# Remove old aliases
sed -i.backup '/# Claude Code auto-logging/,+6d' ~/.zshrc

# Add corrected aliases
cat >> ~/.zshrc << 'EOF'

# Claude Code auto-logging (fixed version)
alias cc-prog='claude'
alias cc-prog-c='claude --continue'
alias cc-prog-skip='claude --dangerously-skip-permissions'
alias cc-prog-c-skip='claude --continue --dangerously-skip-permissions'
alias cc-prog-r='claude --resume'
alias cc-prog-r-skip='claude --resume --dangerously-skip-permissions'
EOF

echo "✅ Aliases fixed!"
echo ""
echo "⚠️  NOTE: tee logging doesn't work well with interactive Claude sessions"
echo "   The aliases now work normally WITHOUT auto-logging."
echo ""
echo "   For session logging, Claude Code has built-in session persistence."
echo "   Check: ~/.config/claude-code/sessions/ for session history"
echo ""
echo "🔄 Reload your shell:"
echo "   source ~/.zshrc"
