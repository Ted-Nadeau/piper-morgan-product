#!/bin/bash

# Secret Detection Script - Find exposed API keys across all repos
# =================================================================

echo "🔍 Scanning all repositories for exposed secrets..."
echo "=================================================="

# Define your project paths
PROJECTS=(
    "$HOME/Development/piper-morgan-platform"
    "$HOME/Development/layersofmeta" 
    "$HOME/Development/one-job"
)

# Common secret patterns to search for
PATTERNS=(
    "api_key"
    "API_KEY"
    "secret"
    "SECRET"
    "token"
    "TOKEN"
    "password"
    "PASSWORD"
    "sk-"          # OpenAI API key prefix
    "ghp_"         # GitHub personal access token
    "gho_"         # GitHub OAuth token
    "ghu_"         # GitHub user token
    "ghs_"         # GitHub server token
    "ghr_"         # GitHub refresh token
    "AKIA"         # AWS Access Key prefix
    "ASIA"         # AWS Session Token prefix
)

# Function to check a single repository
check_repo() {
    local repo_path=$1
    local repo_name=$(basename "$repo_path")
    
    if [ ! -d "$repo_path" ]; then
        echo "❌ Repository not found: $repo_path"
        return
    fi
    
    echo ""
    echo "🔍 Checking: $repo_name"
    echo "----------------------------------------"
    
    cd "$repo_path" || return
    
    # Check if it's a git repository
    if [ ! -d ".git" ]; then
        echo "⚠️  Not a git repository: $repo_path"
        return
    fi
    
    # Check git history for secrets
    echo "📜 Scanning git history..."
    for pattern in "${PATTERNS[@]}"; do
        results=$(git log --all --full-history -p -S "$pattern" --oneline 2>/dev/null)
        if [ -n "$results" ]; then
            echo "🚨 FOUND '$pattern' in git history:"
            echo "$results" | head -5
            echo ""
        fi
    done
    
    # Check current working directory files
    echo "📁 Scanning current files..."
    for pattern in "${PATTERNS[@]}"; do
        results=$(grep -r "$pattern" . --exclude-dir=.git --exclude-dir=node_modules 2>/dev/null)
        if [ -n "$results" ]; then
            echo "🚨 FOUND '$pattern' in current files:"
            echo "$results" | head -5
            echo ""
        fi
    done
    
    # Check what files are currently tracked
    echo "📋 Currently tracked sensitive files:"
    git ls-tree -r HEAD --name-only | grep -E '\.(env|json|key|pem|config)$' | while read file; do
        echo "⚠️  Tracked: $file"
        # Show first few lines to identify if it contains secrets
        head -3 "$file" 2>/dev/null | grep -E '(key|secret|token|password)' && echo "  ^ Contains potential secrets!"
    done
}

# Main execution
echo "Starting comprehensive secret scan..."
echo "This will check git history AND current files"
echo ""

for project in "${PROJECTS[@]}"; do
    check_repo "$project"
done

echo ""
echo "🏁 Scan complete!"
echo ""
echo "Next steps if secrets were found:"
echo "1. Note which repositories and files contained secrets"
echo "2. Remove those specific files from git tracking"
echo "3. Add proper .gitignore entries"
echo "4. Regenerate ALL exposed API keys"
echo "5. Consider using 'git filter-branch' for complete history cleanup"
