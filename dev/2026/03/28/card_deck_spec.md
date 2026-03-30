# One Job Card Deck Experience - Implementation Spec

**Target**: iPhone-optimized mobile interface
**Metaphor**: Physical deck of playing cards
**Philosophy**: Minimal, ceremonial, focused interaction

## 🎯 Core Design Principles

1. **Decluttered by default**: All text/UI chrome removed from viewport
2. **Card deck metaphor**: Tasks as playing cards in a physical stack
3. **Ceremonial interaction**: Intentional tapping to reveal tasks
4. **Auto-behavior with timeouts**: Smart revealing/hiding based on user activity
5. **Spatial thinking**: Foundation for future domain-based navigation

## 📱 Viewport Structure

### Three-Element Layout
1. **Background Canvas**: Minimal margin around central object
2. **Card Stack**: Takes up ~80-90% of viewport real estate
3. **Hidden Menu**: Accessible via long-press, no permanent UI

### Visual Hierarchy
- Card stack is the dominant visual element
- Background provides subtle framing
- No permanent text, buttons, or navigation chrome

## 🃏 Card States & Interactions

### Initial State
- **Face-down deck** with One Job logo on card back
- **Subtle pulse hint** (first launch only) suggesting interactivity
- **Static logo** - no task count or other information

### Primary Interactions

#### 1. Tap to Reveal
- **Trigger**: Tap on face-down card
- **Action**: Card flips over smoothly to reveal current task
- **Animation**: Choose randomly from 3-4 flip variations (energy-efficient CSS)

#### 2. Swipe Right (Complete)
- **Behavior**: Task completed, moves to Done stack
- **Next card**: Auto-flips immediately to show next task
- **Timeout**: Auto-closes after 1 minute of inactivity

#### 3. Swipe Left (Defer)
- **Behavior**: Card flips face-down, moves to bottom of stack
- **Next card**: Auto-flips immediately to show next task
- **Timeout**: Auto-closes after 1 minute of inactivity

#### 4. Tap Face-Up Card (Detail View)
- **Trigger**: Tap anywhere on revealed card
- **Action**: Card expands to full viewport
- **Styling**: Maintains card-like visual qualities (shadows, borders, rounded corners)
- **Content**: Full task details, substacks, editing capabilities
- **Persistence**: Stays open indefinitely until manually closed
- **Exit**: Tap outside card affordances → shrinks back to deck size, resumes timeout

#### 5. Long-Press Menu
- **Trigger**: Long-press on deck (any state)
- **Menu Items**:
  - ➕ **Add New Task**
  - 🔄 **To Done Stack** (switch to completed tasks view)
  - 🔗 **Integrations**
  - ⚙️ **Settings**
- **Layout**: Floating action buttons in arc/cluster around deck
- **Dismissal**: Tap elsewhere or select option

## ⏱️ Timeout Behavior

### Auto-Close Rules
- **Duration**: 1 minute of inactivity
- **Triggers timeout**:
  - No taps, swipes, or other interactions
  - Card remains face-up
- **Action**: Card flips face-down smoothly
- **Resume**: Tap to reveal again

### Exceptions (No Timeout)
- Card in expanded detail view
- Long-press menu is open
- User is actively editing task details

## 🎭 Animation System

### Card Flip Variations
Create 3-4 different flip animations:
1. **Classic flip**: Rotation around Y-axis
2. **Quick snap**: Faster rotation with slight bounce
3. **Smooth turn**: Slower, more deliberate rotation
4. **Gentle wave**: Y-axis rotation with subtle X-axis tilt

### Implementation Notes
- Use CSS transforms for performance
- Random selection on each flip
- Maintain consistent timing (~300-400ms)
- Energy-efficient (no excessive repaints)

## 🏗️ Empty State Design

### No Tasks Available
- **Visual**: Dashed outline where card deck would be
- **Message**: Cheerful text suggesting user is fortunate to have no tasks
- **Primary Action**: Plus button for adding new task
- **Secondary Action**: Long-press plus button reveals full menu
- **Styling**: Maintains minimal aesthetic, encouraging rather than anxious

## 📋 V1 Navigation Scope

### Current Implementation
- **Main Stack**: Current task deck (primary interface)
- **Done Stack**: Completed tasks (accessible via long-press menu)
- **Simple Toggle**: Back and forth between main and done
- **Integrations**: Separate menu item

### Future Vision (Reference Only)
- Spatial domains (home/work/projects)
- Each domain contains main + done + substacks
- Hierarchical navigation where substacks use parent as canvas
- More sophisticated spatial metaphors

## 🔧 Technical Requirements

### Performance Priorities
1. Smooth 60fps animations
2. Efficient memory usage
3. Fast touch response
4. Minimal battery drain

### Mobile Optimizations
- Touch target sizes (minimum 44px)
- Swipe gesture thresholds
- Prevent scroll bounce
- Handle orientation changes gracefully

### Accessibility
- VoiceOver support for card states
- Haptic feedback for key interactions
- High contrast mode compatibility
- Large text support

## 🎨 Visual Design Notes

### Card Appearance
- **Face-down**: One Job logo, coral/minimal color scheme
- **Face-up**: Clean task presentation, readable typography
- **Expanded**: Full-viewport with card-like styling (shadows, rounded corners)

### Color & Typography
- Maintain existing coral minimal design system
- Inter font family
- High contrast for readability
- Consistent with current brand

### Shadows & Depth
- Subtle drop shadows to enhance card metaphor
- Depth changes during animations
- Stack appearance when multiple cards visible

## 🚀 Implementation Priority

### Phase 1 (Core Experience)
1. Basic card flip interaction
2. Swipe gestures (complete/defer)
3. Auto-flip after actions
4. Timeout behavior
5. Long-press menu

### Phase 2 (Polish)
1. Animation variations
2. Expanded detail view
3. Empty state design
4. Performance optimization

### Phase 3 (Navigation)
1. Done stack toggle
2. Integration with existing backend
3. Settings interface

---

**End of Spec** - Ready for Claude Code implementation with Q&A support.
