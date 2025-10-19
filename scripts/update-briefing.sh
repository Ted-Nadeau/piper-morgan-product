#!/bin/bash
# scripts/update-briefing.sh
# Automated briefing position and status updater
# Usage: ./scripts/update-briefing.sh [--position 2.3.5] [--auto]

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# File paths
BRIEFING_FILE="docs/briefing/BRIEFING-CURRENT-STATE.md"
BACKUP_FILE="docs/briefing/BRIEFING-CURRENT-STATE.md.backup"

# Helper functions
print_header() {
    echo -e "${BLUE}================================${NC}"
    echo -e "${BLUE}  Briefing Update Tool${NC}"
    echo -e "${BLUE}================================${NC}"
    echo
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# Get current position from file
get_current_position() {
    grep "^\*\*Current Position\*\*:" "$BRIEFING_FILE" | \
        sed 's/.*: \([0-9.]*\).*/\1/' | head -1
}

# Get current timestamp from file
get_current_timestamp() {
    grep "^\*\*Last Updated\*\*:" "$BRIEFING_FILE" | \
        sed 's/.*: \(.*\)/\1/' | head -1
}

# Increment position intelligently
increment_position() {
    local pos=$1
    local major=$(echo $pos | cut -d. -f1)
    local minor=$(echo $pos | cut -d. -f2)
    local patch=$(echo $pos | cut -d. -f3)

    # Increment patch version
    patch=$((patch + 1))
    echo "${major}.${minor}.${patch}"
}

# Derive sprint from position
# 2.3.1 = A1, 2.3.2 = CRAFT, 2.3.3 = A2, 2.3.4 = A3, etc.
derive_sprint() {
    local pos=$1
    local patch=$(echo $pos | cut -d. -f3)

    case $patch in
        1) echo "A1" ;;
        2) echo "CRAFT" ;;
        3) echo "A2" ;;
        4) echo "A3" ;;
        5) echo "A4" ;;
        6) echo "A5" ;;
        7) echo "A6" ;;
        8) echo "A7" ;;
        9) echo "A8" ;;
        *) echo "A?" ;;
    esac
}

# Generate timestamp
generate_timestamp() {
    date +"%B %d, %Y, %-I:%M %p %Z"
}

# Main script
main() {
    print_header

    # Check if file exists
    if [ ! -f "$BRIEFING_FILE" ]; then
        print_error "Briefing file not found: $BRIEFING_FILE"
        exit 1
    fi

    # Get current values
    current_pos=$(get_current_position)
    current_ts=$(get_current_timestamp)
    suggested_pos=$(increment_position "$current_pos")
    current_sprint=$(derive_sprint "$current_pos")
    suggested_sprint=$(derive_sprint "$suggested_pos")

    echo "Current position: $current_pos (Sprint $current_sprint)"
    echo "Current timestamp: $current_ts"
    echo

    # Parse command line args
    AUTO_MODE=false
    NEW_POS=""

    while [[ $# -gt 0 ]]; do
        case $1 in
            --position)
                NEW_POS="$2"
                shift 2
                ;;
            --auto)
                AUTO_MODE=true
                shift
                ;;
            --help)
                echo "Usage: $0 [--position X.Y.Z] [--auto]"
                echo ""
                echo "Options:"
                echo "  --position X.Y.Z  Set specific position (e.g., 2.3.5)"
                echo "  --auto            Use suggested position without prompts"
                echo "  --help            Show this help message"
                exit 0
                ;;
            *)
                print_error "Unknown option: $1"
                echo "Use --help for usage information"
                exit 1
                ;;
        esac
    done

    # Determine new position
    if [ -n "$NEW_POS" ]; then
        new_pos="$NEW_POS"
    elif [ "$AUTO_MODE" = true ]; then
        new_pos="$suggested_pos"
    else
        # Interactive prompt
        echo -e "${YELLOW}What is the new position?${NC}"
        echo "  [Enter] = $suggested_pos (suggested)"
        echo "  Or type a custom position (e.g., 2.3.5)"
        read -p "> " user_input

        if [ -z "$user_input" ]; then
            new_pos="$suggested_pos"
        else
            new_pos="$user_input"
        fi
    fi

    new_sprint=$(derive_sprint "$new_pos")
    new_ts=$(generate_timestamp)

    echo
    print_success "New position: $new_pos (Sprint $new_sprint)"
    print_success "New timestamp: $new_ts"
    echo

    # Create backup
    cp "$BRIEFING_FILE" "$BACKUP_FILE"
    print_success "Created backup: $BACKUP_FILE"

    # Update the file
    # Update position line
    sed -i '' "s/^\*\*Current Position\*\*: ${current_pos} .*$/\*\*Current Position\*\*: ${new_pos} (Complete the Build of CORE - Sprint ${new_sprint} Active)/" "$BRIEFING_FILE"

    # Update timestamp
    sed -i '' "s/^\*\*Last Updated\*\*: .*$/\*\*Last Updated\*\*: ${new_ts}/" "$BRIEFING_FILE"

    # Update inchworm location
    sed -i '' "s/^Position ${current_pos} =/Position ${new_pos} =/" "$BRIEFING_FILE"

    print_success "Updated BRIEFING-CURRENT-STATE.md"
    echo

    # Show diff
    echo -e "${BLUE}Changes made:${NC}"
    echo "---"
    diff "$BACKUP_FILE" "$BRIEFING_FILE" || true
    echo "---"
    echo

    # Verify symlink propagation
    if [ -L "knowledge/BRIEFING-CURRENT-STATE.md" ]; then
        print_success "Symlink verified - changes propagate to knowledge/"
    else
        print_warning "knowledge/BRIEFING-CURRENT-STATE.md is not a symlink"
    fi

    echo
    echo -e "${GREEN}Update complete!${NC}"
    echo
    echo "Next steps:"
    echo "  1. Review changes above"
    echo "  2. If correct, commit: git add docs/briefing/BRIEFING-CURRENT-STATE.md"
    echo "  3. Or revert: cp $BACKUP_FILE $BRIEFING_FILE"
    echo "  4. Clean up backup: rm $BACKUP_FILE"
    echo
}

# Run main function
main "$@"
