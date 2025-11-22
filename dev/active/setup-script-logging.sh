#!/bin/bash
# Setup Claude Code logging using macOS 'script' command
# This works with interactive sessions unlike 'tee'

echo "🔧 Setting up Claude Code session logging with 'script' command..."
echo ""

# Remove old broken tee aliases
if grep -q "# Claude Code auto-logging" ~/.zshrc 2>/dev/null; then
    echo "📝 Removing old tee-based aliases..."
    # Create backup
    cp ~/.zshrc ~/.zshrc.backup-$(date +%Y%m%d-%H%M%S)
    # Remove old section
    sed -i '' '/# Claude Code auto-logging/,/^alias cc-prog-r-skip/d' ~/.zshrc
    echo "✅ Old aliases removed (backup created)"
fi

# Add new script-based aliases
echo ""
echo "📝 Adding new script-based aliases..."

cat >> ~/.zshrc << 'EOF'

# Claude Code with session logging (using script command)
# Usage: cc-prog, cc-prog-c, cc-prog-skip, etc.

# Helper function to create log directory
_cc_logdir() {
    local logdir=~/Development/piper-morgan/dev/archive/$(date +%Y/%m/%d)
    mkdir -p "$logdir"
    echo "$logdir/$(date +%Y-%m-%d-%H%M)-prog-code-raw.txt"
}

# Basic session
alias cc-prog='script -q $(_cc_logdir) claude'

# Continue last session
alias cc-prog-c='script -q $(_cc_logdir) claude --continue'

# Skip permissions
alias cc-prog-skip='script -q $(_cc_logdir) claude --dangerously-skip-permissions'

# Continue + skip
alias cc-prog-c-skip='script -q $(_cc_logdir) claude --continue --dangerously-skip-permissions'

# Resume session
alias cc-prog-r='script -q $(_cc_logdir) claude --resume'

# Resume + skip
alias cc-prog-r-skip='script -q $(_cc_logdir) claude --resume --dangerously-skip-permissions'

# View today's logs
alias cc-logs='ls -lah ~/Development/piper-morgan/dev/archive/$(date +%Y/%m/%d)/'

# Read last log (strips script control codes)
alias cc-last='cat $(ls -t ~/Development/piper-morgan/dev/archive/$(date +%Y/%m/%d)/*.txt 2>/dev/null | head -1) | col -b | tail -n 100'
EOF

echo "✅ New aliases added!"
echo ""
echo "🔄 Reloading shell..."
source ~/.zshrc

echo ""
echo "✅ Setup complete!"
echo ""
echo "🚀 Usage:"
echo "   claude                    → cc-prog"
echo "   claude --continue         → cc-prog-c"
echo "   claude --dangerously...   → cc-prog-skip"
echo "   claude -c --dangerous...  → cc-prog-c-skip"
echo "   claude --resume           → cc-prog-r"
echo "   claude --resume --dang... → cc-prog-r-skip"
echo ""
echo "📁 Logs saved to:"
echo "   ~/Development/piper-morgan/dev/archive/YYYY/MM/DD/*.txt"
echo ""
echo "📋 View logs:"
echo "   cc-logs      - List today's logs"
echo "   cc-last      - Show last 100 lines of most recent log"
echo ""
echo "⚠️  Note: To exit Claude AND stop logging, type 'exit' in Claude"
echo ""
