#!/bin/bash
# Fix the script-based aliases - make them work at runtime

echo "🔧 Fixing script-based aliases..."

# Remove the broken aliases
sed -i '' '/# Claude Code with session logging/,/alias cc-last=/d' ~/.zshrc

# Add corrected versions
cat >> ~/.zshrc << 'EOF'

# Claude Code with session logging (using script command)
# Fixed version - log directory created at runtime

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

# View today's logs
alias cc-logs='ls -lah ~/Development/piper-morgan/dev/archive/$(date +%Y/%m/%d)/'

# Read last log (strips script control codes)
alias cc-last='cat $(ls -t ~/Development/piper-morgan/dev/archive/$(date +%Y/%m/%d)/*.txt 2>/dev/null | head -1) 2>/dev/null | col -b | tail -n 100'
EOF

echo "✅ Aliases fixed!"
echo ""
echo "🔄 Reload your shell:"
echo "   source ~/.zshrc"
echo ""
echo "🚀 Then try:"
echo "   cc-prog-c-skip"
echo ""
