#!/bin/bash
# One-time setup script for Claude Code tee logging
# Run this once: bash dev/active/setup-tee-logging.sh

echo "🔧 Setting up Claude Code auto-logging..."
echo ""

# Check if alias already exists
if grep -q "alias cc-prog=" ~/.zshrc 2>/dev/null; then
    echo "✅ Alias already exists in ~/.zshrc"
else
    echo "📝 Adding aliases to ~/.zshrc..."
    echo "" >> ~/.zshrc
    echo "# Claude Code auto-logging (added by setup script)" >> ~/.zshrc
    echo "alias cc-prog='claude 2>&1 | tee ~/Development/piper-morgan/dev/archive/\$(date +%Y/%m/%d)/\$(date +%Y-%m-%d-%H%M)-prog-code-raw.txt'" >> ~/.zshrc
    echo "alias cc-prog-c='claude --continue 2>&1 | tee ~/Development/piper-morgan/dev/archive/\$(date +%Y/%m/%d)/\$(date +%Y-%m-%d-%H%M)-prog-code-raw.txt'" >> ~/.zshrc
    echo "alias cc-prog-skip='claude --dangerously-skip-permissions 2>&1 | tee ~/Development/piper-morgan/dev/archive/\$(date +%Y/%m/%d)/\$(date +%Y-%m-%d-%H%M)-prog-code-raw.txt'" >> ~/.zshrc
    echo "alias cc-prog-c-skip='claude --continue --dangerously-skip-permissions 2>&1 | tee ~/Development/piper-morgan/dev/archive/\$(date +%Y/%m/%d)/\$(date +%Y-%m-%d-%H%M)-prog-code-raw.txt'" >> ~/.zshrc
    echo "alias cc-prog-r='claude --resume 2>&1 | tee ~/Development/piper-morgan/dev/archive/\$(date +%Y/%m/%d)/\$(date +%Y-%m-%d-%H%M)-prog-code-raw.txt'" >> ~/.zshrc
    echo "alias cc-prog-r-skip='claude --resume --dangerously-skip-permissions 2>&1 | tee ~/Development/piper-morgan/dev/archive/\$(date +%Y/%m/%d)/\$(date +%Y-%m-%d-%H%M)-prog-code-raw.txt'" >> ~/.zshrc
    echo "✅ Aliases added to ~/.zshrc"
fi

echo ""
echo "🔄 Reloading shell configuration..."
source ~/.zshrc

echo ""
echo "✅ Setup complete!"
echo ""
echo "📋 Test it:"
echo "   alias cc-prog"
echo ""
echo "🚀 Usage:"
echo "   Instead of:  claude                         → Type: cc-prog"
echo "   Instead of:  claude -c                      → Type: cc-prog-c"
echo "   Instead of:  claude --dangerously-skip-...  → Type: cc-prog-skip"
echo "   Instead of:  claude -c --dangerous...       → Type: cc-prog-c-skip"
echo "   Instead of:  claude --resume                → Type: cc-prog-r"
echo "   Instead of:  claude --resume --dangerous... → Type: cc-prog-r-skip"
echo ""
echo "📁 Raw logs will be saved to:"
echo "   dev/archive/YYYY/MM/DD/YYYY-MM-DD-HHMM-prog-code-raw.txt"
echo ""
