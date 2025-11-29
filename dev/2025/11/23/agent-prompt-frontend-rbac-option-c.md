# Code Agent Prompt: Option C - Conversational Permission Commands

**Date**: November 23, 2025, 12:55 PM
**Estimated Duration**: 30 minutes
**Foundation**: Option B complete (permissions.js, sharing modals, resource pages)

---

## Your Mission

Add natural language shortcuts for permission actions. Users can say things like:
- "share my project plan with alex as editor"
- "who can access my todos?"
- "show me lists michelle shared with me"

You're building on top of working infrastructure from Option B - reuse existing modals and permission helpers.

---

## Context: What Already Exists (Option B)

✅ **Permission System**:
- `web/static/js/permissions.js` - Helper functions (canEdit, canDelete, canShare, getUserRole)
- `web/static/css/permissions.css` - Badge styles
- `window.currentUser` with is_admin flag

✅ **UI Components**:
- Sharing modal (opens via `openShareModal(resourceType, resourceId, resourceName)`)
- Resource pages: `/lists`, `/todos`, `/projects`
- Permission-aware buttons

✅ **Backend APIs**:
- `POST /api/v1/{resource_type}/{id}/share` - Add share
- `DELETE /api/v1/{resource_type}/{id}/share/{user_id}` - Remove share
- `GET /api/v1/{resource_type}/{id}/shares` - List current shares

---

## What You Need to Build

### Part 1: Find the Conversational Interface

**First, locate where user messages are processed:**

```bash
# Find chat/message handling code
grep -r "sendMessage\|handleMessage\|processMessage\|onSubmit" web/static/js/ --include="*.js"

# Look for input handlers
grep -r "addEventListener.*input\|addEventListener.*submit" web/static/js/ --include="*.js"

# Find existing intent/command system
grep -r "intent\|command\|parse" web/static/js/ --include="*.js"
```

**Document your findings** in comments before proceeding.

---

### Part 2: Add Intent Parsing Functions

Add to the appropriate JavaScript file (likely `web/static/js/chat.js` or `web/static/js/main.js`):

```javascript
/**
 * Parse sharing commands from natural language
 * Examples:
 *   - "share my project plan with alex@example.com as editor"
 *   - "give michelle access to todos as viewer"
 *   - "let sara edit my list"
 */
function parseShareCommand(text) {
  const patterns = [
    // "share X with Y as Z"
    /share (my )?(\w+)\s+(.+?)\s+with ([\w@\.\-\+]+)(?: as (\w+))?/i,
    // "give X access to Y"
    /give ([\w@\.\-\+]+) access to (my )?(\w+)\s+(.+?)(?: as (\w+))?/i,
    // "let X edit/view Y"
    /let ([\w@\.\-\+]+) (view|edit|manage) (my )?(\w+)\s+(.+)/i,
  ];

  for (const pattern of patterns) {
    const match = text.match(pattern);
    if (match) {
      // Extract components based on pattern match
      let resourceType, resourceName, recipientEmail, role;

      if (pattern.source.includes('share')) {
        resourceType = match[2]; // 'project', 'list', 'todo'
        resourceName = match[3]; // 'plan', 'shopping list'
        recipientEmail = match[4];
        role = match[5] || 'VIEWER';
      } else if (pattern.source.includes('give')) {
        recipientEmail = match[1];
        resourceType = match[3];
        resourceName = match[4];
        role = match[5] || 'VIEWER';
      } else if (pattern.source.includes('let')) {
        recipientEmail = match[1];
        const action = match[2]; // 'view', 'edit', 'manage'
        resourceType = match[4];
        resourceName = match[5];
        role = actionToRole(action);
      }

      return {
        intent: 'share',
        resourceType: normalizeResourceType(resourceType),
        resourceName: resourceName?.trim(),
        recipientEmail: recipientEmail?.trim(),
        role: role?.toUpperCase() || 'VIEWER'
      };
    }
  }
  return null;
}

/**
 * Parse permission query commands
 * Examples:
 *   - "who can access my project plan?"
 *   - "show me shared lists"
 *   - "what are my permissions on todos?"
 */
function parsePermissionQuery(text) {
  const patterns = [
    // "who can access X"
    /who (can access|has access to) (my )?(\w+)\s*(.+)?/i,
    // "show shared X"
    /show (me )?(my )?shared (\w+)s?/i,
    // "what are my permissions"
    /what are (my )?permissions (on|for) (my )?(\w+)\s*(.+)?/i,
    // "list X shared with/by me"
    /(list|show) (\w+)s? shared (with|by) me/i,
  ];

  for (const pattern of patterns) {
    const match = text.match(pattern);
    if (match) {
      let resourceType, resourceName, filter;

      if (pattern.source.includes('who')) {
        resourceType = match[3];
        resourceName = match[4]?.trim();
        filter = 'shares';
      } else if (pattern.source.includes('show')) {
        resourceType = match[3];
        filter = 'shared-with-me';
      } else if (pattern.source.includes('permissions')) {
        resourceType = match[4];
        resourceName = match[5]?.trim();
        filter = 'my-role';
      } else if (pattern.source.includes('list')) {
        resourceType = match[2];
        filter = match[3] === 'with' ? 'shared-with-me' : 'shared-by-me';
      }

      return {
        intent: 'permission_query',
        resourceType: normalizeResourceType(resourceType),
        resourceName: resourceName,
        filter: filter
      };
    }
  }
  return null;
}

// Helper functions
function normalizeResourceType(type) {
  const normalized = type?.toLowerCase().replace(/s$/, ''); // Remove trailing 's'
  const typeMap = {
    'list': 'lists',
    'todo': 'todos',
    'project': 'projects'
  };
  return typeMap[normalized] || type;
}

function actionToRole(action) {
  const actionMap = {
    'view': 'VIEWER',
    'edit': 'EDITOR',
    'manage': 'ADMIN'
  };
  return actionMap[action.toLowerCase()] || 'VIEWER';
}
```

---

### Part 3: Add Intent Handlers

```javascript
/**
 * Handle sharing intent - opens sharing modal with pre-filled values
 */
async function handleShareIntent(intent) {
  const { resourceType, resourceName, recipientEmail, role } = intent;

  try {
    // If resource name provided, search for it
    let resourceId;
    if (resourceName) {
      const response = await fetch(`/api/v1/${resourceType}?search=${encodeURIComponent(resourceName)}`);
      const resources = await response.json();

      if (resources.length === 0) {
        return {
          success: false,
          message: `Could not find ${resourceType.slice(0, -1)} named "${resourceName}"`
        };
      }

      // Use first match
      const resource = resources[0];
      resourceId = resource.id;

      // Check permissions
      if (!canShare(resource)) {
        return {
          success: false,
          message: `You don't have permission to share "${resource.name}"`
        };
      }

      // Open sharing modal (from Option B)
      openShareModal(resourceType, resourceId, resource.name);

      // Pre-fill recipient if provided
      if (recipientEmail) {
        // Wait for modal to render
        setTimeout(() => {
          const emailInput = document.getElementById('share-user-input');
          const roleSelect = document.getElementById('share-role-select');
          if (emailInput) emailInput.value = recipientEmail;
          if (roleSelect) roleSelect.value = role;
        }, 100);
      }

      return {
        success: true,
        message: `Opening share dialog for "${resource.name}"`
      };
    } else {
      // No specific resource - show resource page
      window.location.href = `/${resourceType}`;
      return {
        success: true,
        message: `Showing your ${resourceType} - click Share on the one you want to share`
      };
    }
  } catch (error) {
    console.error('Share intent error:', error);
    return {
      success: false,
      message: `Error processing share command: ${error.message}`
    };
  }
}

/**
 * Handle permission query intent - shows who has access
 */
async function handlePermissionQueryIntent(intent) {
  const { resourceType, resourceName, filter } = intent;

  try {
    if (filter === 'shared-with-me' || filter === 'shared-by-me') {
      // Navigate to resource page (it already shows shared resources)
      window.location.href = `/${resourceType}`;
      return {
        success: true,
        message: `Showing your ${resourceType} (including shared)`
      };
    }

    if (resourceName) {
      // Query specific resource
      const response = await fetch(`/api/v1/${resourceType}?search=${encodeURIComponent(resourceName)}`);
      const resources = await response.json();

      if (resources.length === 0) {
        return {
          success: false,
          message: `Could not find ${resourceType.slice(0, -1)} named "${resourceName}"`
        };
      }

      const resource = resources[0];
      const userRole = getUserRole(resource);

      let message = `**${resource.name}**\n\n`;
      message += `Your role: ${formatRole(userRole)}\n\n`;

      if (resource.shared_with && resource.shared_with.length > 0) {
        message += "Shared with:\n";
        resource.shared_with.forEach(share => {
          message += `- ${share.username || share.user_id} (${formatRole(share.role)})\n`;
        });
      } else {
        message += "Not shared with anyone.";
      }

      return {
        success: true,
        message: message
      };
    } else {
      // Show resource page
      window.location.href = `/${resourceType}`;
      return {
        success: true,
        message: `Showing your ${resourceType}`
      };
    }
  } catch (error) {
    console.error('Permission query error:', error);
    return {
      success: false,
      message: `Error querying permissions: ${error.message}`
    };
  }
}
```

---

### Part 4: Integrate with Message Handler

Find where user messages are processed and add this logic:

```javascript
async function processUserMessage(message) {
  const text = message.trim();

  // Try parsing as sharing command
  const shareIntent = parseShareCommand(text);
  if (shareIntent) {
    const result = await handleShareIntent(shareIntent);
    displayResponse(result.message);
    return;
  }

  // Try parsing as permission query
  const queryIntent = parsePermissionQuery(text);
  if (queryIntent) {
    const result = await handlePermissionQueryIntent(queryIntent);
    displayResponse(result.message);
    return;
  }

  // Fall back to existing conversational AI
  await sendToConversationalAI(message);
}
```

---

## Testing Checklist

Before committing, test these commands in the chat interface:

### Sharing Commands
- [ ] "share my project plan with alex@example.com as editor"
- [ ] "give michelle access to todos as viewer"
- [ ] "let sara edit my shopping list"
- [ ] "share list" (no name - should show lists page)

### Permission Queries
- [ ] "who can access my project plan?"
- [ ] "show me shared lists"
- [ ] "what are my permissions on todos?"
- [ ] "list projects shared with me"

### Error Handling
- [ ] Non-existent resource name (should show friendly error)
- [ ] Try to share resource you don't own (should deny gracefully)
- [ ] Malformed commands (should fall back to conversational AI)

---

## Validation Commands

```bash
# Run pre-commit checks
./scripts/fix-newlines.sh
git add .
git commit -m "feat(#376): Add conversational permission commands (Option C)

- Add natural language parsing for sharing commands
- Add permission query intents
- Integrate with Option B sharing modals
- Support commands like 'share X with Y as Z'

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"

# Test in browser console
parseShareCommand("share my project plan with alex@example.com as editor")
// Should return: {intent: 'share', resourceType: 'projects', resourceName: 'plan', recipientEmail: 'alex@example.com', role: 'EDITOR'}

parsePermissionQuery("who can access my todos?")
// Should return: {intent: 'permission_query', resourceType: 'todos', filter: 'shares'}
```

---

## Success Criteria

**Before reporting complete**:
- [ ] Sharing commands open existing Option B modals
- [ ] Permission queries show accurate information
- [ ] Commands don't conflict with normal chat
- [ ] Error messages are clear and helpful
- [ ] No JavaScript console errors
- [ ] Pre-commit hooks pass
- [ ] Code follows existing patterns in codebase

---

## STOP Conditions

**STOP and report if**:
- Can't find conversational interface code
- Message handling system is completely different than expected
- Option B modals not accessible from JavaScript
- Breaking changes to existing chat functionality
- Pattern matching causes conflicts with normal conversation

---

## Reporting Back

When complete, provide:
1. **Files modified** with line counts
2. **Commit hash** from git log
3. **Test results** - which commands you validated
4. **Any issues encountered** and how you resolved them
5. **Console validation** - paste results of parser tests

---

**Remember**:
- Reuse Option B infrastructure (don't duplicate code)
- Maintain existing conversational AI functionality
- Permission checks before all actions
- Clear error messages for users
- Michelle arrives tomorrow - keep it simple!

---

*Prompt prepared by: Lead Developer*
*Date: November 23, 2025, 12:55 PM*
*Estimated completion: 1:30 PM*
