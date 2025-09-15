#!/bin/bash

# Piper Morgan Dock Icon Setup Script
# Adds icon with dark/light mode support

echo "🎨 Setting up Piper Morgan dock icon with dark/light mode support..."
echo "📦 Version 2.0.0 - Enhanced for Issue #163 startup process changes"
echo ""

# Check if app already exists and offer to replace it
if [ -d ~/Applications/PiperMorgan.app ]; then
    echo "⚠️  Existing PiperMorgan.app found - will be replaced with updated version"
    rm -rf ~/Applications/PiperMorgan.app
fi

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Create app bundle structure
echo "📁 Creating application bundle..."
mkdir -p ~/Applications/PiperMorgan.app/Contents/{MacOS,Resources}

# Create the Info.plist file with icon configuration
echo "📝 Creating Info.plist..."
cat > ~/Applications/PiperMorgan.app/Contents/Info.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>PiperMorgan</string>
    <key>CFBundleIconFile</key>
    <string>AppIcon</string>
    <key>CFBundleIdentifier</key>
    <string>com.pipermorgan.app</string>
    <key>CFBundleName</key>
    <string>Piper Morgan</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0</string>
    <key>CFBundleVersion</key>
    <string>1</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.15</string>
    <key>NSHighResolutionCapable</key>
    <true/>
</dict>
</plist>
EOF

# Create the enhanced launcher script
echo "🚀 Creating enhanced launcher script..."
cat > ~/Applications/PiperMorgan.app/Contents/MacOS/PiperMorgan << EOF
#!/bin/bash

# Piper Morgan Enhanced Dock Launcher
# Version: 2.0.0 - Updated for Issue #163 startup process changes
# Purpose: Robust one-click startup with comprehensive error handling

set -e  # Exit on any error

# Set up environment for GUI launch
export PATH="/usr/local/bin:/usr/bin:/bin:/opt/homebrew/bin:\$PATH"

# Preserve important environment variables
if [ -n "\$GITHUB_TOKEN" ]; then
    export GITHUB_TOKEN="\$GITHUB_TOKEN"
fi

# Navigate to project directory
PROJECT_DIR="$SCRIPT_DIR/.."
cd "\$PROJECT_DIR"

# Verify we're in the right place
if [ ! -f "scripts/start-piper.sh" ]; then
    echo "❌ Error: Cannot find startup script at \$(pwd)/scripts/start-piper.sh"
    echo "Please ensure you're launching from the correct Piper Morgan directory."
    read -p "Press Enter to exit..."
    exit 1
fi

# Check if startup script is executable
if [ ! -x "scripts/start-piper.sh" ]; then
    echo "🔧 Making startup script executable..."
    chmod +x scripts/start-piper.sh
fi

echo "🚀 Launching Piper Morgan from \$(pwd)..."
echo "📍 Using startup script: scripts/start-piper.sh"
echo ""

# Launch startup script in a new terminal window with proper environment
# Use AppleScript to create a new terminal window with the startup command
osascript << 'APPLESCRIPT'
tell application "Terminal"
    activate
    set newWindow to do script "cd '$SCRIPT_DIR/..' && export GITHUB_TOKEN='\$GITHUB_TOKEN' && ./scripts/start-piper.sh"
    set custom title of newWindow to "Piper Morgan Startup"
end tell
APPLESCRIPT

echo "✅ Piper Morgan startup initiated in new Terminal window"
EOF

# Make launcher executable
chmod +x ~/Applications/PiperMorgan.app/Contents/MacOS/PiperMorgan

# Convert PNG to ICNS format for macOS
echo "🎨 Creating icon set..."

# First, check if we have the logo
if [ ! -f "$SCRIPT_DIR/../docs/pm-logo.png" ]; then
    echo "⚠️  Warning: pm-logo.png not found at $SCRIPT_DIR/../docs/pm-logo.png"
    echo "The app will work but won't have a custom icon."
else
    # Create iconset directory
    ICONSET_DIR=~/Applications/PiperMorgan.app/Contents/Resources/AppIcon.iconset
    mkdir -p "$ICONSET_DIR"

    # Create different sizes needed for macOS icon
    # Using sips (built into macOS) to resize
    echo "📐 Creating icon sizes..."

    # Copy original as base
    cp "$SCRIPT_DIR/../docs/pm-logo.png" "$ICONSET_DIR/icon_512x512@2x.png"

    # Generate all required sizes
    sips -z 1024 1024 "$ICONSET_DIR/icon_512x512@2x.png" --out "$ICONSET_DIR/icon_512x512@2x.png" >/dev/null 2>&1
    sips -z 512 512 "$ICONSET_DIR/icon_512x512@2x.png" --out "$ICONSET_DIR/icon_512x512.png" >/dev/null 2>&1
    sips -z 512 512 "$ICONSET_DIR/icon_512x512@2x.png" --out "$ICONSET_DIR/icon_256x256@2x.png" >/dev/null 2>&1
    sips -z 256 256 "$ICONSET_DIR/icon_512x512@2x.png" --out "$ICONSET_DIR/icon_256x256.png" >/dev/null 2>&1
    sips -z 256 256 "$ICONSET_DIR/icon_512x512@2x.png" --out "$ICONSET_DIR/icon_128x128@2x.png" >/dev/null 2>&1
    sips -z 128 128 "$ICONSET_DIR/icon_512x512@2x.png" --out "$ICONSET_DIR/icon_128x128.png" >/dev/null 2>&1
    sips -z 64 64 "$ICONSET_DIR/icon_512x512@2x.png" --out "$ICONSET_DIR/icon_32x32@2x.png" >/dev/null 2>&1
    sips -z 32 32 "$ICONSET_DIR/icon_512x512@2x.png" --out "$ICONSET_DIR/icon_32x32.png" >/dev/null 2>&1
    sips -z 32 32 "$ICONSET_DIR/icon_512x512@2x.png" --out "$ICONSET_DIR/icon_16x16@2x.png" >/dev/null 2>&1
    sips -z 16 16 "$ICONSET_DIR/icon_512x512@2x.png" --out "$ICONSET_DIR/icon_16x16.png" >/dev/null 2>&1

    # Convert iconset to icns
    echo "🔨 Building icon file..."
    iconutil -c icns "$ICONSET_DIR" -o ~/Applications/PiperMorgan.app/Contents/Resources/AppIcon.icns

    # Clean up iconset directory
    rm -rf "$ICONSET_DIR"

    echo "✅ Icon created successfully!"
fi

# Create a dark mode variant script (optional enhancement)
echo "🌓 Setting up dark/light mode support..."
cat > ~/Applications/PiperMorgan.app/Contents/Resources/check-appearance.sh << 'EOF'
#!/bin/bash
# Check if dark mode is enabled
DARK_MODE=$(defaults read -g AppleInterfaceStyle 2>/dev/null)
if [ "$DARK_MODE" = "Dark" ]; then
    echo "dark"
else
    echo "light"
fi
EOF
chmod +x ~/Applications/PiperMorgan.app/Contents/Resources/check-appearance.sh

echo "✅ Enhanced Application bundle created successfully!"
echo ""
echo "🆕 What's New in Version 2.0.0:"
echo "   • Updated for new startup process (Issue #163 fixes)"
echo "   • Robust error handling and environment preservation"
echo "   • Proper GITHUB_TOKEN environment variable handling"
echo "   • Enhanced Terminal integration with custom window titles"
echo "   • Automatic startup script permission management"
echo ""
echo "📌 To add to your dock:"
echo "   1. Open Finder and go to ~/Applications"
echo "   2. Find PiperMorgan.app"
echo "   3. Drag it to your dock"
echo ""
echo "🎨 Note: The dolphin logo adapts well to both dark and light modes"
echo "   due to its cyan/turquoise color scheme with black outlines."
echo ""
echo "🧪 Testing:"
echo "   • Double-click the app in ~/Applications to test it first"
echo "   • The app will open a new Terminal window with Piper Morgan startup"
echo "   • Check that all services start correctly (backend on :8001, frontend on :8081)"
echo ""
echo "🔧 Troubleshooting:"
echo "   • If startup fails, check that Docker Desktop is running"
echo "   • Ensure GITHUB_TOKEN is set in your shell environment"
echo "   • Verify virtual environment exists in the project directory"
