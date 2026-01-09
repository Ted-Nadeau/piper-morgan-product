# Piper Mobile PoC Session Log

**Date:** 2026-01-03
**Role:** Vibe Coding Agent (Skunkworks)
**Task:** Deploy gestural interaction PoC to iPhone

## Session Context

Continuing from Dec 27 session where we:
- Built native iOS app via Xcode
- Enabled Developer Mode on iPhone
- App installed but couldn't launch due to certificate trust issue
- User reports they may have solved the developer feature issue

## Previous Blockers (Dec 27)

1. Device certificate not appearing in VPN & Device Management
2. "Internet connection" error when launching app
3. Gestures not triggering in Simulator (may be threshold issue)

---

## Progress Log

### 3:55 PM - Session Start

User ready to retry iPhone deployment. Certificate issue may be resolved.

---

## Quick Reference: Deploy to iPhone

**Option A: Via Xcode (recommended)**
```bash
# Open the Xcode project
open /Users/xian/Development/piper-morgan/skunkworks/mobile/piper-mobile-poc/ios/PiperMobile.xcworkspace
```
Then:
1. Select "Port Monteau" (your iPhone) from device dropdown
2. Press Cmd+R to build and run

**Option B: Via command line**
```bash
cd /Users/xian/Development/piper-morgan/skunkworks/mobile/piper-mobile-poc
npx expo run:ios --device
```

---

## Session Notes

### 3:55 PM - 4:09 PM Progress

**What worked:**
- Opened Xcode project successfully
- Selected iPhone "Port Monteau" as target device
- Build succeeded
- App installed on device
- Splash screen appeared on phone (native app is working!)

**Current blockers:**
- USB connection unstable (handshake timeout errors)
- Xcode debugger can't attach to running app
- Wireless debugging also failing to connect
- USB hub may be causing issues - direct connection attempted

**Next step:**
- User restarting laptop to reset USB/Xcode state
- Then retry direct USB connection and Cmd+R build

### Status: Paused for laptop restart (4:09 PM)

---

### 5:27 PM - Back from errands

- Retried build, encountered Xcode warnings (third-party libs - not blocking)
- Discovered phone and laptop on different subnets
- Fixed network - both on same WiFi now

### 6:01 PM - BREAKTHROUGH

- App loads! "Gesture Lab" screen visible on phone
- User can disconnect USB cable - app runs via WiFi to Metro

### 6:02 PM - Bug discovered

- Cards animate when swiped but no toast appears
- User requests systematic "five whys" debugging per CLAUDE.md

### 6:15 PM - Root cause found

**Gestures ARE working!** Metro logs prove intents fire:
```
LOG  [Intent] task:Review Q1 roadmap draft → swipeRight → complete
LOG  [Intent] task:Review Q1 roadmap draft → swipeLeft → defer
LOG  [Intent] project:Mobile 2.0 Initiative → swipeUp → addMilestone
```

**Real bug:** IntentToast not visible (not gesture detection)

**Root cause:** Toast uses `position: 'absolute'` but lacks `zIndex`, so it renders behind ScrollView.

**Fix applied:** Added `zIndex: 1000` to IntentToast container style.

---

## Technical State Summary

- **Native iOS build**: Working (compiles, installs)
- **App on device**: Running via WiFi
- **Metro bundler**: Running on 192.168.4.150:8081
- **Gesture detection**: WORKING (verified via Metro logs)
- **Toast visibility**: Fix applied, awaiting verification
