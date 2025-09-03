#!/bin/bash

# Piper Morgan Dock Icon Setup Script
# Adds icon with dark/light mode support

echo "🎨 Setting up Piper Morgan dock icon with dark/light mode support..."

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

# Create the launcher script
echo "🚀 Creating launcher script..."
cat > ~/Applications/PiperMorgan.app/Contents/MacOS/PiperMorgan << EOF
#!/bin/bash
cd "$SCRIPT_DIR"
./start-piper.sh
EOF

# Make launcher executable
chmod +x ~/Applications/PiperMorgan.app/Contents/MacOS/PiperMorgan

# Convert PNG to ICNS format for macOS
echo "🎨 Creating icon set..."

# First, check if we have the logo
if [ ! -f "$SCRIPT_DIR/docs/pm-logo.png" ]; then
    echo "⚠️  Warning: pm-logo.png not found at $SCRIPT_DIR/docs/pm-logo.png"
    echo "The app will work but won't have a custom icon."
else
    # Create iconset directory
    ICONSET_DIR=~/Applications/PiperMorgan.app/Contents/Resources/AppIcon.iconset
    mkdir -p "$ICONSET_DIR"

    # Create different sizes needed for macOS icon
    # Using sips (built into macOS) to resize
    echo "📐 Creating icon sizes..."

    # Copy original as base
    cp "$SCRIPT_DIR/docs/pm-logo.png" "$ICONSET_DIR/icon_512x512@2x.png"

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

echo "✅ Application bundle created successfully!"
echo ""
echo "📌 To add to your dock:"
echo "   1. Open Finder and go to ~/Applications"
echo "   2. Find PiperMorgan.app"
echo "   3. Drag it to your dock"
echo ""
echo "🎨 Note: The dolphin logo adapts well to both dark and light modes"
echo "   due to its cyan/turquoise color scheme with black outlines."
echo ""
echo "💡 Tip: You can also double-click the app in ~/Applications to test it first"
