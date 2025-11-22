#!/bin/bash
# Clean ALL old Claude aliases and add working versions

echo "🔧 Cleaning up ALL old Claude Code aliases..."

# Backup .zshrc
cp ~/.zshrc ~/.zshrc.backup-$(date +%Y%m%d-%H%M%S)
echo "✅ Backup created: ~/.zshrc.backup-$(date +%Y%m%d-%H%M%S)"

# Remove ALL Claude Code related sections
sed -i '' '/# Claude Code auto-logging/,/^$/d' ~/.zshrc
sed -i '' '/# Claude Code with session logging/,/^$/d' ~/.zshrc
sed -i '' '/^alias cc-prog/d' ~/.zshrc
sed -i '' '/^cc-prog()/,/^}/d' ~/.zshrc
sed -i '' '/^cc-prog-c()/,/^}/d' ~/.zshrc
sed -i '' '/^cc-prog-skip()/,/^}/d' ~/.zshrc
sed -i '' '/^cc-prog-c-skip()/,/^}/d' ~/.zshrc
sed -i '' '/^cc-prog-r()/,/^}/d' ~/.zshrc
sed -i '' '/^cc-prog-r-skip()/,/^}/d' ~/.zshrc
sed -i '' '/^alias cc-logs/d' ~/.zshrc
sed -i '' '/^alias cc-last/d' ~/.zshrc

echo "✅ Old aliases removed"
echo ""

# Add clean new functions
echo "📝 Adding new working functions..."

cat >> ~/.zshrc << 'EOF'

# Claude Code with session logging
# Usage: cc-prog, cc-prog-c, cc-prog-skip, cc-prog-c-skip, cc-prog-r, cc-prog-r-skip

cc-prog() {
    local logdir=~/Development/piper-morgan/dev/archive/$(date +%Y/%m/%d)
    mkdir -p "$logdir"
    script -q "$logdir/$(date +%Y-%m-%d-%H%M)-prog-code-raw.txt" claude
}

cc-prog-c() {
    local logdir=~/Development/piper-morgan/dev/archive/$(date +%Y/%m/%d)
    mkdir -p "$logdir"
    script -q "$logdir/$(date +%Y-%m-%d-%H%M)-prog-code-raw.txt" claude --continue
}

cc-prog-skip() {
    local logdir=~/Development/piper-morgan/dev/archive/$(date +%Y/%m/%d)
    mkdir -p "$logdir"
    script -q "$logdir/$(date +%Y-%m-%d-%H%M)-prog-code-raw.txt" claude --dangerously-skip-permissions
}

cc-prog-c-skip() {
    local logdir=~/Development/piper-morgan/dev/archive/$(date +%Y/%m/%d)
    mkdir -p "$logdir"
    script -q "$logdir/$(date +%Y-%m-%d-%H%M)-prog-code-raw.txt" claude --continue --dangerously-skip-permissions
}

cc-prog-r() {
    local logdir=~/Development/piper-morgan/dev/archive/$(date +%Y/%m/%d)
    mkdir -p "$logdir"
    script -q "$logdir/$(date +%Y-%m-%d-%H%M)-prog-code-raw.txt" claude --resume
}

cc-prog-r-skip() {
    local logdir=~/Development/piper-morgan/dev/archive/$(date +%Y/%m/%d)
    mkdir -p "$logdir"
    script -q "$logdir/$(date +%Y-%m-%d-%H%M)-prog-code-raw.txt" claude --resume --dangerously-skip-permissions
}

alias cc-logs='ls -lah ~/Development/piper-morgan/dev/archive/$(date +%Y/%m/%d)/'
alias cc-last='cat $(ls -t ~/Development/piper-morgan/dev/archive/$(date +%Y/%m/%d)/*.txt 2>/dev/null | head -1) 2>/dev/null | col -b | tail -n 100'

EOF

echo "✅ New functions added!"
echo ""
echo "🔄 IMPORTANT: Close this terminal and open a NEW terminal window"
echo "   (or run: exec zsh)"
echo ""
echo "🚀 Then test with:"
echo "   cc-prog-c-skip"
echo ""
