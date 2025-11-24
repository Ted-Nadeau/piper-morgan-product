# Gameplan: Option C - Conversational Permission Commands
**Issue**: #376 FRONTEND-RBAC-AWARENESS (Extension)
**Date**: November 23, 2025, 12:51 PM
**Decision**: Add conversational commands after Option B success
**Estimated Duration**: 20-30 minutes
**Target**: Complete today for Michelle tomorrow

---

## Mission Statement

Add natural language shortcuts for permission-aware actions, leveraging existing UI components from Option B. Enable power users and accessibility through conversational interface.

**Foundation**: Option B infrastructure complete (permissions.js, sharing modals, resource pages)

---

## Known Issue to Track

**Login/Logout UI Missing**: No visible authentication interface in current UI
- **Severity**: Medium (Michelle will need instructions for alpha)
- **Workaround**: Provide direct login URL or instructions
- **Future Work**: Add login/logout buttons to navigation
- **For Now**: Document in alpha onboarding guide (Issue #377)

---

## Phase 1: Intent Handler Extensions (15 minutes)

### Objective
Add permission-aware intent handlers to existing conversational system

### Tasks

**1.1 Locate existing intent system** (2 min)
```bash
# Find intent handler code
grep -r "handleIntent\|processIntent" web/static/js/ services/
```

**1.2 Add sharing intent handler** (8 min)

Add to intent processing system:
```javascript
// Handle: "share my project plan with alex as editor"
// Handle: "share list X with user@example.com as viewer"
// Handle: "give michelle access to my todos"

async function handleShareIntent(intent) {
  const { resourceType, resourceId, recipientEmail, role } = intent;

  // Validate permissions first
  const resource = await fetchResource(resourceType, resourceId);
  if (!canShare(resource)) {
    return {
      success: false,
      message: "You don't have permission to share this resource."
    };
  }

  // Open sharing modal from Option B
  openShareModal(resourceType, resourceId, resource.name);

  // Pre-fill with parsed values if available
  if (recipientEmail) {
    document.getElementById('share-user-input').value = recipientEmail;
  }
  if (role) {
    document.getElementById('share-role-select').value = role.toUpperCase();
  }

  return {
    success: true,
    message: `Opening share dialog for ${resource.name}`
  };
}
```

**1.3 Add permission query intent** (5 min)

```javascript
// Handle: "who can access my project plan?"
// Handle: "show me lists michelle shared with me"
// Handle: "what are my permissions on list X?"

async function handlePermissionQueryIntent(intent) {
  const { resourceType, resourceId } = intent;

  const resource = await fetchResource(resourceType, resourceId);
  const userRole = getUserRole(resource);

  let response = `Your role: ${formatRole(userRole)}\n\n`;

  if (resource.shared_with && resource.shared_with.length > 0) {
    response += "Shared with:\n";
    resource.shared_with.forEach(share => {
      response += `- ${share.username} (${formatRole(share.role)})\n`;
    });
  } else {
    response += "Not shared with anyone.";
  }

  return {
    success: true,
    message: response
  };
}
```

---

## Phase 2: NLP Parsing Patterns (10 minutes)

### Objective
Add pattern matching for permission-related commands

### Tasks

**2.1 Sharing command patterns** (5 min)

Add to NLP parser:
```javascript
const sharingPatterns = [
  // Basic sharing
  /share (my )?(\w+) (?:with|to) ([\w@\.\-]+)(?: as (\w+))?/i,
  // "give X access to Y"
  /give ([\w@\.\-]+) access to (my )?(\w+)(?: as (\w+))?/i,
  // "let X edit Y"
  /let ([\w@\.\-]+) (view|edit|manage) (my )?(\w+)/i,
];

function parseShareCommand(text) {
  for (const pattern of sharingPatterns) {
    const match = text.match(pattern);
    if (match) {
      return {
        intent: 'share',
        resourceType: extractResourceType(match),
        recipientEmail: extractRecipient(match),
        role: extractRole(match) || 'VIEWER'
      };
    }
  }
  return null;
}
```

**2.2 Permission query patterns** (5 min)

```javascript
const permissionQueryPatterns = [
  /who (can access|has access to) (my )?(\w+)/i,
  /what are (my )?permissions (on|for) (\w+)/i,
  /show (me )?(my )?shared (\w+)s?/i,
  /(list|show) (\w+)s? shared (with|by) me/i,
];

function parsePermissionQuery(text) {
  for (const pattern of permissionQueryPatterns) {
    const match = text.match(pattern);
    if (match) {
      return {
        intent: 'permission_query',
        resourceType: extractResourceType(match),
        filter: extractFilter(match) // 'shared-with-me' or 'shared-by-me'
      };
    }
  }
  return null;
}
```

---

## Phase 3: Integration & Testing (5 minutes)

### Objective
Wire conversational commands to existing Option B UI

### Tasks

**3.1 Connect intents to modals** (3 min)

Ensure conversational commands trigger same UI as button clicks:
```javascript
// Chat input handler
async function processUserMessage(message) {
  // Try parsing as sharing command
  const shareIntent = parseShareCommand(message);
  if (shareIntent) {
    await handleShareIntent(shareIntent);
    return;
  }

  // Try parsing as permission query
  const queryIntent = parsePermissionQuery(message);
  if (queryIntent) {
    await handlePermissionQueryIntent(queryIntent);
    return;
  }

  // Fall back to existing conversational AI
  await sendToConversationalAI(message);
}
```

**3.2 Quick validation** (2 min)

Test in browser console:
```javascript
// Test share command parsing
parseShareCommand("share my project plan with alex@example.com as editor");
// Expected: {intent: 'share', resourceType: 'project', recipientEmail: 'alex@example.com', role: 'EDITOR'}

// Test permission query
parsePermissionQuery("who can access my todos?");
// Expected: {intent: 'permission_query', resourceType: 'todo'}
```

---

## Acceptance Criteria

### Functionality
- [ ] "share X with Y as Z" opens sharing modal with pre-filled values
- [ ] "who can access X" shows current shares
- [ ] "show shared lists" filters to shared resources
- [ ] Permission checks prevent unauthorized sharing attempts
- [ ] Commands work alongside existing button-based UI

### Quality
- [ ] No conflicts with existing conversational AI
- [ ] Error messages clear and helpful
- [ ] Pattern matching handles variations (my/the, with/to, etc.)
- [ ] Integrates with Option B modals (no duplicate code)

### Documentation
- [ ] Session log updated
- [ ] Known issue documented (login/logout UI)

---

## Success Criteria

**Option B + C Together**:
- ✅ Resource pages exist and work (/lists, /todos, /projects)
- ✅ Permission-aware buttons hide/show correctly
- ✅ Sharing modal functional
- ✅ Conversational shortcuts work ("share X with Y")
- ✅ Both approaches use same permission system
- ⚠️ Login/logout UI documented as known issue for Issue #377

---

## Timeline Estimate

| Phase | Task | Time | Cumulative |
|-------|------|------|------------|
| 1 | Intent handlers | 15 min | 15 min |
| 2 | NLP patterns | 10 min | 25 min |
| 3 | Integration & testing | 5 min | 30 min |

**Total**: 30 minutes (with buffer: ~35-40 minutes)

**Start**: 12:55 PM
**Estimated Complete**: 1:30 PM

---

## Known Issues to Track

### Login/Logout UI Missing
- **What**: No visible login/logout buttons in navigation
- **Impact**: Michelle will need manual instructions for alpha
- **Workaround**: Document in Issue #377 (alpha docs)
- **Future**: Add to navigation bar (post-alpha)
- **Action**: Note in alpha onboarding guide

---

## STOP Conditions

**STOP immediately if**:
- Intent system doesn't exist or is completely different
- Conversational AI conflicts with new patterns
- Permission checks fail in conversational context
- Breaking changes to Option B modals

---

## Next Steps After Option C

1. **Issue #377** (ALPHA-DOCS-UPDATE):
   - Document login/logout workaround
   - Add permission system to user guide
   - Update known issues list

2. **Issue #378** (ALPHA-DEPLOY-PROD):
   - Deploy Option B + C to production
   - Run smoke tests
   - Verify Michelle can access

---

**Gameplan Status**: ✅ Ready for execution
**Foundation**: ✅ Option B complete (permissions.js, modals, pages)
**Approach**: Lightweight layer over existing infrastructure

---

*Gameplan prepared by: Lead Developer*
*Date: November 23, 2025, 12:51 PM*
*For: Code Agent (quick implementation)*
