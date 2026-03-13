# Piper Mobile PoC Session Log

**Date:** 2025-12-27
**Role:** Vibe Coding Agent (Skunkworks)
**Task:** Debug gesture triggers, deploy to physical iPhone

## Session Context

Continuing from Dec 23/25 sessions:
- Native iOS build works, app runs in Simulator
- Cards animate when dragged but snap back without triggering intents
- User has Apple Developer account - ready for device deployment

## Current Issue

**Symptom:** Cards wobble/animate when dragged, then return to position. No intent toast appears.

**Expected:** When dragged past threshold (~100px), should:
1. Show intent label overlay on card
2. Trigger haptic feedback
3. Fire intent and show toast at bottom
4. Card snaps back after intent fires

**Hypothesis:** Either:
1. Drag distance not reaching commit threshold (100px)
2. Intent callback not connected
3. Toast component not rendering
4. Gesture end handler not firing intent

---

## Progress Log

### 8:29 PM - Session Start

Investigating gesture behavior. Need to review:
- `src/gestures/gestureConfig.ts` - threshold settings
- `src/components/EntityCard.tsx` - gesture handlers and callbacks
- `src/screens/GestureLabScreen.tsx` - intent handling and toast display

---

## Session Notes

### 8:29 PM - 10:05 PM Session Progress

**Accomplished:**
- Reviewed gesture code - logic looks correct (100px threshold for commit)
- Restarted Metro with cache clear
- Opened project in Xcode for device deployment
- Accepted Xcode modernization updates
- Fixed User Script Sandboxing (changed to No)
- Enabled Developer Mode on iPhone
- App successfully built and installed to device

**Blockers Encountered:**
1. **Simulator gestures**: User dragged full length of phone, still no intent triggered - suspicious
2. **Device certificate**: App installed but certificate not appearing in VPN & Device Management
3. **"Internet connection" error**: Misleading error when trying to launch on device
4. **Simulator window not appearing**: Build says "Running" but no window visible

**Current State:**
- Xcode project configured with sandboxing disabled
- Developer Mode enabled on iPhone (Port Monteau)
- App installed on device but can't launch (certificate trust issue)
- Simulator build runs but window may need to be opened manually

### To Resume Tomorrow:

1. **Simulator first**:
   - Open Simulator app manually (Applications → Xcode → Open Developer Tool → Simulator)
   - Or: `open -a Simulator` from terminal
   - Then build from Xcode (Cmd+R)
   - Test drag gestures (click-hold-drag ~100px)

2. **If gestures still don't work in Simulator**:
   - Add debug logging to gesture handlers
   - Check if Metro is serving latest bundle
   - Consider lowering threshold temporarily for testing

3. **For device deployment**:
   - Try `npx expo prebuild --clean` to regenerate iOS folder
   - Or try revoking and regenerating certificates in Xcode
   - May need to check Apple Developer account status (free vs paid)

---

## Session End: 10:05 PM

**Status**: Paused - resume debugging tomorrow morning
